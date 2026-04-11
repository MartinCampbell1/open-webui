<script lang="ts">
	import { getContext } from 'svelte';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import FolderOpen from '$lib/components/icons/FolderOpen.svelte';
	import ClockRotateRight from '$lib/components/icons/ClockRotateRight.svelte';
	import ChatBubbleDotted from '$lib/components/icons/ChatBubbleDotted.svelte';
	import AdjustmentsHorizontal from '$lib/components/icons/AdjustmentsHorizontal.svelte';
	import QueueList from '$lib/components/icons/QueueList.svelte';

	type TaskState = 'idle' | 'running' | 'approval' | 'tasks';

	export let taskState: TaskState = 'idle';
	export let count = 0;
	export let showLiveRun = true;

	export let onWorkspace = () => {};
	export let onCurrentContext = () => {};
	export let onSessionHistory = () => {};
	export let onInspect = () => {};
	export let onLiveRun = () => {};

	const i18n = getContext<any>('i18n');

	$: hasLiveRun = showLiveRun;
	$: liveRunTone =
		taskState === 'approval'
			? 'approval'
			: taskState === 'running'
				? 'running'
				: taskState === 'tasks'
					? 'tasks'
					: 'idle';
	$: liveRunLabel =
		liveRunTone === 'approval'
			? `${$i18n.t('Live run')} · ${$i18n.t('Pending approval')}`
			: liveRunTone === 'running'
				? `${$i18n.t('Live run')} · ${$i18n.t('Running')}`
				: liveRunTone === 'tasks'
					? `${$i18n.t('Live run')} · ${$i18n.t('Tasks')}`
					: $i18n.t('Live run');
	$: liveRunCountLabel = count > 99 ? '99+' : String(Math.max(0, count));

	const baseActionClass =
		'flex min-h-9 min-w-9 cursor-pointer items-center gap-1.5 rounded-lg px-2.5 py-2 text-sm leading-5 text-gray-700 transition touch-manipulation select-none hover:bg-white hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-300/80 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-gray-100 dark:focus-visible:ring-gray-600/80 dark:focus-visible:ring-offset-gray-850';
	const liveRunBaseClass =
		'group relative flex min-h-9 min-w-9 cursor-pointer items-center gap-1.5 rounded-lg px-2.5 py-2 text-sm leading-5 transition touch-manipulation select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-300/80 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:focus-visible:ring-gray-600/80 dark:focus-visible:ring-offset-gray-850';
</script>

<div
	class="inline-flex max-w-full items-center gap-1 rounded-xl bg-gray-50/70 p-1 dark:bg-gray-850/70 ring-1 ring-gray-200/70 dark:ring-gray-800/70"
>
	<Tooltip content={$i18n.t('Workspace')}>
		<button
			type="button"
			class={baseActionClass}
			on:click={onWorkspace}
			aria-label={$i18n.t('Workspace')}
		>
			<FolderOpen className="size-4" />
			<span class="hidden lg:inline">{$i18n.t('Workspace')}</span>
		</button>
	</Tooltip>

	<Tooltip content={$i18n.t('Current context')}>
		<button
			type="button"
			class={baseActionClass}
			on:click={onCurrentContext}
			aria-label={$i18n.t('Current context')}
		>
			<ClockRotateRight className="size-4" />
			<span class="hidden lg:inline">{$i18n.t('Current context')}</span>
		</button>
	</Tooltip>

	<Tooltip content={$i18n.t('Session history')}>
		<button
			type="button"
			class={baseActionClass}
			on:click={onSessionHistory}
			aria-label={$i18n.t('Session history')}
		>
			<ChatBubbleDotted className="size-4" strokeWidth="1.75" />
			<span class="hidden lg:inline">{$i18n.t('Session history')}</span>
		</button>
	</Tooltip>

	<Tooltip content={$i18n.t('Inspect')}>
		<button
			type="button"
			class={baseActionClass}
			on:click={onInspect}
			aria-label={$i18n.t('Inspect')}
		>
			<AdjustmentsHorizontal className="size-4" />
			<span class="hidden lg:inline">{$i18n.t('Inspect')}</span>
		</button>
	</Tooltip>

	{#if hasLiveRun}
		<Tooltip content={liveRunLabel}>
			<button
				type="button"
				class={`${liveRunBaseClass} ${
					liveRunTone === 'approval'
						? 'bg-amber-500/10 text-amber-700 hover:bg-amber-500/15 dark:bg-amber-400/15 dark:text-amber-200 dark:hover:bg-amber-400/20'
						: liveRunTone === 'running'
							? 'bg-emerald-500/10 text-emerald-700 hover:bg-emerald-500/15 dark:bg-emerald-400/15 dark:text-emerald-200 dark:hover:bg-emerald-400/20'
							: liveRunTone === 'tasks'
								? 'bg-sky-500/10 text-sky-700 hover:bg-sky-500/15 dark:bg-sky-400/15 dark:text-sky-200 dark:hover:bg-sky-400/20'
								: 'text-gray-700 hover:bg-white hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-gray-100'
				}`}
				on:click={onLiveRun}
				aria-label={$i18n.t('Live run')}
			>
				<span class="relative flex size-4 items-center justify-center">
					<QueueList className="size-4" />
					{#if liveRunTone === 'running'}
						<span
							class="absolute -right-0.5 -top-0.5 size-2 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-gray-850 animate-pulse"
							aria-hidden="true"
						/>
					{:else if liveRunTone === 'approval'}
						<span
							class="absolute -right-0.5 -top-0.5 size-2 rounded-full bg-amber-500 ring-2 ring-white dark:ring-gray-850"
							aria-hidden="true"
						/>
					{:else if liveRunTone === 'tasks'}
						<span
							class="absolute -right-0.5 -top-0.5 size-2 rounded-full bg-sky-500 ring-2 ring-white dark:ring-gray-850"
							aria-hidden="true"
						/>
					{/if}
				</span>
				<span class="hidden lg:inline">{$i18n.t('Live run')}</span>
				{#if count > 0}
					<span
						class="hidden xl:inline-flex items-center rounded-full px-1.5 py-0.5 text-[11px] font-medium leading-none
							{liveRunTone === 'approval'
							? 'bg-amber-500/15 text-amber-700 dark:bg-amber-400/20 dark:text-amber-100'
							: liveRunTone === 'running'
								? 'bg-emerald-500/15 text-emerald-700 dark:bg-emerald-400/20 dark:text-emerald-100'
								: liveRunTone === 'tasks'
									? 'bg-sky-500/15 text-sky-700 dark:bg-sky-400/20 dark:text-sky-100'
									: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300'}"
					>
						{liveRunCountLabel}
					</span>
				{/if}
				{#if liveRunTone === 'approval'}
					<span class="hidden 2xl:inline text-[11px] font-medium uppercase tracking-[0.16em]">
						{$i18n.t('Approval required')}
					</span>
				{:else if liveRunTone === 'running'}
					<span class="hidden 2xl:inline text-[11px] font-medium uppercase tracking-[0.16em]">
						{$i18n.t('Running')}
					</span>
				{:else if liveRunTone === 'tasks'}
					<span class="hidden 2xl:inline text-[11px] font-medium uppercase tracking-[0.16em]">
						{$i18n.t('Tasks')}
					</span>
				{/if}
			</button>
		</Tooltip>
	{/if}
</div>
