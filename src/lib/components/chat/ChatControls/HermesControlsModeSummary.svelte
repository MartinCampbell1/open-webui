<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	import type { HermesContextSummary } from '$lib/stores';
	import HermesContextBar from '$lib/components/hermes/context/HermesContextBar.svelte';

	const i18n = getContext<any>('i18n');
	const dispatch = createEventDispatcher<{
		workspace: void;
		session: void;
		profile: void;
	}>();

	export type HermesControlsMode = 'operator' | 'inspect';
	export type HermesControlsModeStat = {
		label: string;
		value: string | number;
	};

	export let mode: HermesControlsMode = 'operator';
	export let summary: HermesContextSummary | null = null;
	export let stats: HermesControlsModeStat[] = [];
	export let compact = false;

	const handleWorkspace = () => dispatch('workspace');
	const handleSession = () => dispatch('session');
	const handleProfile = () => dispatch('profile');
</script>

{#if summary}
	<div
		class={`px-3 ${mode === 'operator' ? 'pt-3 pb-2' : 'pt-2.5 pb-1'} ${compact ? 'sm:px-0' : ''}`}
	>
		<div
			class={`rounded-xl ${
				mode === 'operator'
					? 'border border-gray-100/80 bg-white/85 shadow-[0_1px_0_rgba(0,0,0,0.02)] dark:border-gray-800/80 dark:bg-gray-900/55'
					: 'border border-gray-100/60 bg-gray-50/70 dark:border-gray-800/60 dark:bg-gray-900/35'
			} px-3 py-3`}
		>
			<div
				class={`text-[11px] font-medium ${
					mode === 'operator'
						? 'uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500'
						: 'tracking-[0.04em] text-gray-500/80 dark:text-gray-500/75'
				}`}
			>
				{$i18n.t(mode === 'operator' ? 'Current context' : 'Inspect')}
			</div>

			<div class="mt-2">
				<HermesContextBar
					{summary}
					compact={true}
					on:workspace={handleWorkspace}
					on:session={handleSession}
					on:profile={handleProfile}
				/>
			</div>

			{#if mode === 'operator' && stats.length > 0}
				<div class="mt-3 grid grid-cols-2 gap-2">
					{#each stats as stat}
						<div
							class="rounded-xl border border-gray-100/70 bg-gray-50/90 px-3 py-2 dark:border-gray-800/70 dark:bg-gray-950/70"
						>
							<div class="text-[11px] uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500">
								{stat.label}
							</div>
							<div class="mt-1 text-sm font-semibold text-gray-800 dark:text-gray-100">
								{stat.value}
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
{/if}
