<script lang="ts">
	import { getContext } from 'svelte';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import Check from '$lib/components/icons/Check.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';
	import Terminal from '$lib/components/icons/Terminal.svelte';
	import Search from '$lib/components/icons/Search.svelte';
	import GlobeAlt from '$lib/components/icons/GlobeAlt.svelte';
	import FolderOpen from '$lib/components/icons/FolderOpen.svelte';
	import Document from '$lib/components/icons/Document.svelte';
	import PageEdit from '$lib/components/icons/PageEdit.svelte';
	import CodeBracket from '$lib/components/icons/CodeBracket.svelte';

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

	const getToolIcon = (toolName: string) => {
		const normalized = toolName.trim().toLowerCase();

		if (!normalized) {
			return EllipsisHorizontal;
		}

		if (normalized.includes('terminal') || normalized.includes('shell') || normalized.includes('bash')) {
			return Terminal;
		}

		if (normalized.includes('search')) {
			return Search;
		}

		if (normalized.includes('web') || normalized.includes('browser') || normalized.includes('http')) {
			return GlobeAlt;
		}

		if (normalized.includes('read_file') || normalized.includes('file')) {
			return Document;
		}

		if (normalized.includes('patch') || normalized.includes('edit') || normalized.includes('write')) {
			return PageEdit;
		}

		if (normalized.includes('folder') || normalized.includes('directory') || normalized.includes('workspace')) {
			return FolderOpen;
		}

		if (normalized.includes('code') || normalized.includes('python') || normalized.includes('script')) {
			return CodeBracket;
		}

		return EllipsisHorizontal;
	};

	$: toolIcon = getToolIcon(name);
	$: stateLabel =
		state === 'running'
			? $i18n.t('Running')
			: state === 'failed'
				? $i18n.t('Failed')
				: '';
</script>

<div
	class="flex w-full items-center gap-2 rounded-md bg-white/60 transition hover:bg-white/80 dark:bg-white/[0.03] dark:hover:bg-white/[0.05]"
>
	<button
		type="button"
		class="flex min-w-0 flex-1 items-center gap-2 px-2.5 py-1.5 text-left"
		on:click={onClick}
	>
		<div
			class="flex size-5 shrink-0 items-center justify-center rounded-full bg-gray-100/80 text-gray-500 dark:bg-white/[0.06] dark:text-gray-300"
		>
			{#if state === 'running'}
				<Spinner className="size-3" />
			{:else if state === 'failed'}
				<XMark className="size-3" />
			{:else if state === 'done' && toolIcon === EllipsisHorizontal}
				<Check strokeWidth="3" className="size-3" />
			{:else}
				<svelte:component this={toolIcon} class="size-3" />
			{/if}
		</div>

		<div class="min-w-0 flex-1">
			<div class="line-clamp-1 text-sm font-medium text-gray-700 dark:text-gray-200">{name}</div>
			{#if summary}
				<div class="line-clamp-1 text-[11px] leading-4 text-gray-500 dark:text-gray-400">{summary}</div>
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

		{#if stateLabel}
			<div class="shrink-0 text-[11px] text-gray-400 dark:text-gray-500">{stateLabel}</div>
		{/if}
	</button>

	{#if actionLabel}
		<button
			type="button"
			class="mr-2 shrink-0 rounded-full bg-gray-100/80 px-2 py-0.5 text-[11px] font-medium text-gray-500 transition hover:bg-gray-200 hover:text-gray-700 dark:bg-white/[0.06] dark:text-gray-300 dark:hover:bg-white/[0.1]"
			aria-label={actionAriaLabel || actionLabel}
			on:click={onActionClick}
		>
			{actionLabel}
		</button>
	{/if}
</div>
