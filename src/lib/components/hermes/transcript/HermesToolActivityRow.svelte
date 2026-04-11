<script lang="ts">
	import { getContext } from 'svelte';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import Check from '$lib/components/icons/Check.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';

	const i18n = getContext<any>('i18n');

	type ToolState = 'running' | 'done' | 'failed' | 'idle';

	export let name = '';
	export let summary = '';
	export let meta = '';
	export let scopeLabel = '';
	export let state: ToolState = 'idle';
	export let onClick: () => void = () => {};
	export let actionLabel = '';
	export let actionAriaLabel = '';
	export let onActionClick: () => void = () => {};

	const stateConfig: Record<
		ToolState,
		{ label: () => string; row: string; icon: string; chip: string }
	> = {
		running: {
			label: () => $i18n.t('Running'),
			row: 'border-blue-100 bg-blue-50/70 hover:bg-blue-50 dark:border-blue-900/50 dark:bg-blue-950/20 dark:hover:bg-blue-950/30',
			icon: 'bg-blue-100 text-blue-600 dark:bg-blue-950 dark:text-blue-300',
			chip: 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-200'
		},
		done: {
			label: () => $i18n.t('Completed'),
			row: 'border-emerald-100 bg-emerald-50/70 hover:bg-emerald-50 dark:border-emerald-900/50 dark:bg-emerald-950/20 dark:hover:bg-emerald-950/30',
			icon: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-300',
			chip: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-200'
		},
		failed: {
			label: () => $i18n.t('Failed'),
			row: 'border-rose-100 bg-rose-50/70 hover:bg-rose-50 dark:border-rose-900/50 dark:bg-rose-950/20 dark:hover:bg-rose-950/30',
			icon: 'bg-rose-100 text-rose-600 dark:bg-rose-950 dark:text-rose-300',
			chip: 'bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-200'
		},
		idle: {
			label: () => $i18n.t('Idle'),
			row: 'border-gray-100 bg-white/75 hover:bg-white dark:border-gray-800/80 dark:bg-gray-950/70 dark:hover:bg-gray-950',
			icon: 'bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-300',
			chip: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300'
		}
	};

	$: currentState = stateConfig[state] ?? stateConfig.idle;
	$: stateLabel = currentState.label();
</script>

<div class={`flex w-full items-center gap-2 rounded-lg border transition ${currentState.row}`}>
	<button
		type="button"
		class="flex min-w-0 flex-1 items-center gap-2 px-2.5 py-2 text-left"
		on:click={onClick}
	>
		<div
			class={`flex size-5 shrink-0 items-center justify-center rounded-full ${currentState.icon}`}
		>
			{#if state === 'running'}
				<Spinner className="size-3" />
			{:else if state === 'failed'}
				<XMark className="size-3" />
			{:else if state === 'done'}
				<Check strokeWidth="3" className="size-3" />
			{:else}
				<EllipsisHorizontal className="size-3" />
			{/if}
		</div>

		<div class="min-w-0 flex-1">
			<div class="line-clamp-1 text-sm font-medium text-gray-700 dark:text-gray-200">{name}</div>
			{#if summary}
				<div class="line-clamp-1 text-[11px] text-gray-500 dark:text-gray-400">{summary}</div>
			{/if}
			{#if meta || scopeLabel}
				<div class="mt-0.5 flex flex-wrap gap-1.5 text-[11px] text-gray-400 dark:text-gray-500">
					{#if meta}
						<div class="line-clamp-1">{meta}</div>
					{/if}
					{#if scopeLabel}
						<div class="line-clamp-1">{scopeLabel}</div>
					{/if}
				</div>
			{/if}
		</div>

		<div class={`shrink-0 rounded-full px-2 py-0.5 text-[11px] font-medium ${currentState.chip}`}>
			{stateLabel}
		</div>
	</button>

	{#if actionLabel}
		<button
			type="button"
			class="mr-2 shrink-0 rounded-full border border-gray-200 bg-white/70 px-2.5 py-0.5 text-[11px] font-medium text-gray-500 shadow-sm transition hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700 dark:border-gray-700 dark:bg-gray-900/60 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:bg-gray-900"
			aria-label={actionAriaLabel || actionLabel}
			on:click={onActionClick}
		>
			{actionLabel}
		</button>
	{/if}
</div>
