<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	import Dropdown from '$lib/components/common/Dropdown.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';
	import Terminal from '$lib/components/icons/Terminal.svelte';
	import Voice from '$lib/components/icons/Voice.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher<{
		dictate: void;
		note: void;
		terminal: void;
	}>();

	export let show = false;
	export let showDictate = false;
	export let showNote = false;
	export let showTerminal = false;
	export let terminalLabel = '';
	export let disabled = false;
	export let align: 'start' | 'end' = 'end';
	export let side: 'top' | 'bottom' = 'top';

	$: hasActions = showDictate || showNote || showTerminal;
	$: triggerLabel = $i18n.t('Composer actions');

	const closeMenu = () => {
		show = false;
	};

	const emitAction = (action: 'dictate' | 'note' | 'terminal') => {
		dispatch(action);
		closeMenu();
	};
</script>

{#if hasActions}
	<Dropdown bind:show {align} {side} contentClass="z-50">
		<Tooltip content={triggerLabel} placement="top">
			<button
				type="button"
				class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-gray-500 transition hover:bg-gray-50 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-850 dark:hover:text-gray-200 {disabled
					? 'cursor-not-allowed opacity-40 hover:bg-transparent hover:text-gray-500 dark:hover:bg-transparent dark:hover:text-gray-400'
					: 'cursor-pointer'}"
				aria-label={triggerLabel}
				aria-haspopup="menu"
				aria-expanded={show}
				{disabled}
			>
				<EllipsisHorizontal className="size-4" strokeWidth="2" />
			</button>
		</Tooltip>

		<div slot="content">
			<div
				class="min-w-44 rounded-xl border border-gray-100/90 bg-white p-1 shadow-lg dark:border-gray-800/90 dark:bg-gray-850"
			>
				{#if showDictate}
					<button
						type="button"
						class="flex w-full items-center gap-2 rounded-lg px-2.5 py-1.5 text-[13px] text-gray-700 transition hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-gray-800/60"
						on:click={() => emitAction('dictate')}
					>
						<Voice className="size-4 shrink-0 text-gray-500 dark:text-gray-400" />
						<span class="truncate">{$i18n.t('Dictate to Hermes')}</span>
					</button>
				{/if}

				{#if showDictate && (showNote || showTerminal)}
					<hr class="my-1 border-gray-100 dark:border-gray-800" />
				{/if}

				{#if showNote}
					<button
						type="button"
						class="flex w-full items-center gap-2 rounded-lg px-2.5 py-1.5 text-[13px] text-gray-700 transition hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-gray-800/60"
						on:click={() => emitAction('note')}
					>
						<span class="truncate">{$i18n.t('Create Hermes note')}</span>
					</button>
				{/if}

				{#if showNote && showTerminal}
					<hr class="my-1 border-gray-100 dark:border-gray-800" />
				{/if}

				{#if showTerminal}
					<button
						type="button"
						class="flex w-full items-center gap-2 rounded-lg px-2.5 py-1.5 text-[13px] text-gray-700 transition hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-gray-800/60"
						on:click={() => emitAction('terminal')}
					>
						<Terminal className="size-4 shrink-0 text-gray-500 dark:text-gray-400" />
						<div class="min-w-0 text-left">
							<div class="truncate">{$i18n.t('Open terminal files')}</div>
							{#if terminalLabel}
								<div class="truncate text-[11px] text-gray-400 dark:text-gray-500">
									{terminalLabel}
								</div>
							{/if}
						</div>
					</button>
				{/if}
			</div>
		</div>
	</Dropdown>
{/if}
