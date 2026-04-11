<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	import type { HermesContextSummary } from '$lib/stores';
	import HermesContextBar from './HermesContextBar.svelte';

	const i18n = getContext<any>('i18n');
	const dispatch = createEventDispatcher<{
		context: void;
		sessions: void;
		workspace: void;
		tasks: void;
		profile: void;
	}>();

	export let summary: HermesContextSummary | null = null;
	export let compact = false;

	const formatSessionId = (sessionId: string | null | undefined) => {
		if (!sessionId) {
			return '';
		}

		if (sessionId.length <= 14) {
			return sessionId;
		}

		return `${sessionId.slice(0, 8)}…${sessionId.slice(-4)}`;
	};

	$: hasLinkedSession = !!summary?.sessionId;
	$: hasVisibleContext =
		!!summary &&
		(!!summary.sessionId ||
			!!summary.profileLabel ||
			!!summary.workspaceLabel ||
			!!summary.targetId);
	$: stateLabel = summary?.sessionStateLabel ? $i18n.t(summary.sessionStateLabel) : '';
	$: title = hasLinkedSession
		? $i18n.t('Current Hermes context')
		: $i18n.t('Hermes context will attach on the next run');
	$: description = hasLinkedSession
		? $i18n.t(
				'This conversation stays linked to the active runtime context, profile, and workspace.'
			)
		: $i18n.t(
				'The next message will use the current Hermes profile and workspace, then attach the resulting runtime session here.'
			);
	$: metaItems = [
		summary?.sessionId ? `${$i18n.t('Session ID')}: ${formatSessionId(summary.sessionId)}` : '',
		typeof summary?.generatedFileCount === 'number' && summary.generatedFileCount > 0
			? `${$i18n.t('Generated')}: ${summary.generatedFileCount}`
			: '',
		typeof summary?.chatAttachedFileCount === 'number' && summary.chatAttachedFileCount > 0
			? `${$i18n.t('Attached')}: ${summary.chatAttachedFileCount}`
			: '',
		typeof summary?.taskCount === 'number' ? `${$i18n.t('Live run')}: ${summary.taskCount}` : ''
	].filter(Boolean);
</script>

{#if hasVisibleContext && summary}
	<div
		class={`rounded-xl border border-gray-100/80 bg-white/80 dark:border-gray-800/80 dark:bg-gray-900/50 ${
			compact ? 'px-3 py-2.5' : 'px-4 py-3.5'
		}`}
	>
		<div
			class={`flex flex-col gap-3 ${compact ? 'lg:flex-row lg:items-start lg:justify-between' : 'xl:flex-row xl:items-start xl:justify-between'}`}
		>
			<div class="min-w-0">
				<div class="flex flex-wrap items-center gap-2">
					<div
						class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
					>
						{title}
					</div>

					{#if stateLabel}
						<div
							class="rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-gray-600 dark:bg-gray-800 dark:text-gray-300"
						>
							{stateLabel}
						</div>
					{/if}
				</div>

				<div
					class={`text-gray-500 dark:text-gray-400 ${compact ? 'mt-1 text-xs leading-5' : 'mt-1.5 text-sm leading-6'}`}
				>
					{description}
				</div>

				{#if metaItems.length > 0}
					<div class="mt-2 flex flex-wrap gap-1.5">
						{#each metaItems as item}
							<div
								class="rounded-full bg-gray-50 px-2 py-0.5 text-[11px] text-gray-500 dark:bg-gray-950/70 dark:text-gray-400"
							>
								<span class="block max-w-full truncate">{item}</span>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<div class="flex flex-wrap items-center gap-1.5">
				<button
					type="button"
					class={`rounded-full bg-gray-100 font-medium text-gray-700 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700 ${
						compact ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-sm'
					}`}
					on:click={() => dispatch('context')}
				>
					{$i18n.t('Current context')}
				</button>
				<button
					type="button"
					class={`rounded-full bg-gray-100 font-medium text-gray-700 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700 ${
						compact ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-sm'
					}`}
					on:click={() => dispatch('sessions')}
				>
					{$i18n.t('Session history')}
				</button>
				<button
					type="button"
					class={`rounded-full bg-gray-100 font-medium text-gray-700 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700 ${
						compact ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-sm'
					}`}
					on:click={() => dispatch('workspace')}
				>
					{$i18n.t('Workspace')}
				</button>
				<button
					type="button"
					class={`rounded-full bg-gray-100 font-medium text-gray-700 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700 ${
						compact ? 'px-2.5 py-1 text-[11px]' : 'px-3 py-1.5 text-sm'
					}`}
					on:click={() => dispatch('tasks')}
				>
					{$i18n.t('Live run')}
				</button>
			</div>
		</div>

		<div class="mt-2">
			<HermesContextBar
				{summary}
				compact={true}
				on:workspace={() => dispatch('workspace')}
				on:profile={() => dispatch('profile')}
				on:session={() => dispatch('context')}
			/>
		</div>
	</div>
{/if}
