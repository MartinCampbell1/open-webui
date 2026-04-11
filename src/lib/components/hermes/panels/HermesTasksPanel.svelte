<script lang="ts">
	import { getContext } from 'svelte';
	import HermesComposerActivityStrip from '$lib/components/hermes/transcript/HermesComposerActivityStrip.svelte';

	const i18n = getContext<any>('i18n');

	export let active = false;
	export let generating = false;
	export let pendingApproval: Record<string, any> | null = null;
	export let activeModelLabel: string | null = null;
	export let statusLabel: string | null = null;
	export let taskIds: string[] | null = null;
	export let activityMessage: any = null;
	export let statusUpdatesEnabled = true;
	export let stopResponse: Function = async () => {};

	$: visibleTaskIds = taskIds ?? [];
	$: hasTaskHandles = visibleTaskIds.length > 0;
	$: hasActiveRun = generating || hasTaskHandles || !!pendingApproval;
	$: resolvedStatusLabel =
		statusLabel ??
		(pendingApproval
			? $i18n.t('Pending approval')
			: hasActiveRun
				? $i18n.t('Running')
				: $i18n.t('Idle'));
	$: statusTone = pendingApproval
		? 'bg-amber-500'
		: hasActiveRun
			? 'bg-emerald-500'
			: 'bg-gray-300 dark:bg-gray-600';
	$: statusHint = pendingApproval
		? $i18n.t('Approval required')
		: generating
			? $i18n.t('Waiting for result')
			: hasTaskHandles
				? $i18n.t('Running tasks')
				: $i18n.t('Ready');
</script>

<div class="flex h-full min-h-0 flex-col px-2 py-2">
	<div
		class="rounded-2xl border border-gray-100/80 bg-white/80 px-3 py-3 dark:border-gray-800/80 dark:bg-gray-900/50"
	>
		<div class="flex items-start justify-between gap-3">
			<div class="min-w-0">
				<div class="text-sm font-medium text-gray-800 dark:text-gray-100">
					{$i18n.t('Live run')}
				</div>
				<div
					class="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-[11px] text-gray-500 dark:text-gray-400"
				>
					<span class="inline-flex items-center gap-1.5">
						<span class={`inline-flex h-2 w-2 rounded-full ${statusTone}`}></span>
						<span>{resolvedStatusLabel}</span>
					</span>
					<span aria-hidden="true">·</span>
					<span>{statusHint}</span>
					{#if activeModelLabel}
						<span aria-hidden="true">·</span>
						<span class="truncate">{activeModelLabel}</span>
					{/if}
				</div>
			</div>

			<div class="flex shrink-0 items-center gap-2">
				{#if hasActiveRun}
					<button
						type="button"
						class="rounded-full bg-gray-100 px-2.5 py-1 text-[11px] font-medium text-gray-600 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
						on:click={async () => {
							await stopResponse();
						}}
					>
						{$i18n.t('Stop generation')}
					</button>
				{/if}
			</div>
		</div>

		<div class="mt-3 grid gap-2 sm:grid-cols-2">
			<div
				class="rounded-xl border border-gray-100 bg-gray-50/80 px-3 py-2.5 dark:border-gray-800 dark:bg-gray-950/40"
			>
				<div class="text-[10px] uppercase tracking-wide text-gray-400 dark:text-gray-500">
					{$i18n.t('State')}
				</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{resolvedStatusLabel}
				</div>
				<div class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400">
					{statusHint}
				</div>
			</div>

			<div
				class="rounded-xl border border-gray-100 bg-gray-50/80 px-3 py-2.5 dark:border-gray-800 dark:bg-gray-950/40"
			>
				<div class="text-[10px] uppercase tracking-wide text-gray-400 dark:text-gray-500">
					{$i18n.t('Task links')}
				</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{visibleTaskIds.length}
				</div>
				<div class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400">
					{$i18n.t('Active in this chat')}
				</div>
			</div>
		</div>

		{#if pendingApproval}
			<div
				class="mt-3 rounded-xl border border-amber-100/80 bg-amber-50/80 px-3 py-2.5 dark:border-amber-500/20 dark:bg-amber-500/10"
			>
				<div
					class="text-[11px] font-medium uppercase tracking-[0.08em] text-amber-700 dark:text-amber-300"
				>
					{$i18n.t('Approval required')}
				</div>
				<div class="mt-1 text-sm font-medium text-amber-900 dark:text-amber-100">
					{pendingApproval.title ?? $i18n.t('Pending approval')}
				</div>
				{#if pendingApproval.description}
					<div class="mt-1 text-xs leading-5 text-amber-800 dark:text-amber-200">
						{pendingApproval.description}
					</div>
				{/if}
			</div>
		{/if}

		{#if activityMessage}
			<div class="mt-3">
				<div
					class="px-0.5 pb-1 text-[10px] uppercase tracking-wide text-gray-400 dark:text-gray-500"
				>
					{$i18n.t('Latest activity')}
				</div>
				<HermesComposerActivityStrip message={activityMessage} {statusUpdatesEnabled} />
			</div>
		{/if}
	</div>

	<div class="mt-2 flex-1 min-h-0 overflow-y-auto px-1 pb-2">
		{#if !hasActiveRun}
			<div class="px-3 py-5 text-sm text-gray-500 dark:text-gray-400">
				{$i18n.t('No running tasks in this chat.')}
			</div>
		{:else if hasTaskHandles}
			<div class="flex flex-col gap-1.5">
				<div class="px-2 pb-1 text-[10px] uppercase tracking-wide text-gray-400 dark:text-gray-500">
					{$i18n.t('Task references')}
				</div>
				{#each visibleTaskIds as taskId}
					<div
						class="rounded-xl border border-gray-100/80 bg-white/80 px-3 py-2.5 dark:border-gray-800/80 dark:bg-gray-900/50"
					>
						<div class="flex items-center gap-2 text-[11px] text-gray-500 dark:text-gray-400">
							<span
								class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 font-medium dark:bg-gray-800"
							>
								{$i18n.t('Task reference')}
							</span>
							<span class="min-w-0 truncate font-mono text-xs text-gray-700 dark:text-gray-200">
								{taskId}
							</span>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
