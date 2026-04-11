<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	import type { HermesContextSummary } from '$lib/stores';
	import HermesContextBar from './HermesContextBar.svelte';

	const i18n = getContext<any>('i18n');
	const dispatch = createEventDispatcher<{
		workspace: void;
		profile: void;
		session: void;
		tasks: void;
	}>();

	export let summary: HermesContextSummary | null = null;

	$: liveRunState =
		typeof summary?.taskCount === 'number' && summary.taskCount > 0
			? `${summary.taskCount}`
			: $i18n.t('Ready');
</script>

{#if summary}
	<div
		class="rounded-xl border border-gray-100/80 bg-white/80 px-3 py-2.5 dark:border-gray-800/80 dark:bg-gray-900/50"
	>
		<div class="flex items-center justify-between gap-2">
			<div
				class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
			>
				{$i18n.t('Current run context')}
			</div>

			<button
				type="button"
				class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-gray-600 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
				on:click={() => dispatch('tasks')}
			>
				{$i18n.t('Live run')} · {liveRunState}
			</button>
		</div>

		<div class="mt-2">
			<HermesContextBar
				{summary}
				compact={true}
				on:workspace={() => dispatch('workspace')}
				on:profile={() => dispatch('profile')}
				on:session={() => dispatch('session')}
			/>
		</div>
	</div>
{/if}
