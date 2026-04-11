<script lang="ts">
	export type HermesControlsMode = 'operator' | 'inspect';

	export type HermesControlsTab = {
		id: string;
		label: string;
		disabled?: boolean;
	};

	export let mode: HermesControlsMode = 'operator';
	export let tabs: HermesControlsTab[] = [];
	export let activeTab = '';
	export let inspectDisabled = false;
	export let closeLabel = 'Close';
	export let workLabel = 'Work';
	export let inspectLabel = 'Inspect';
	export let title = '';
	export let subtitle = '';
	export let description = '';
	export let modeSubtitle = '';
	export let modeDescription = '';
	export let onSetMode: (nextMode: HermesControlsMode) => void = () => {};
	export let onSetTab: (tabId: string) => void = () => {};
	export let onClose: () => void = () => {};

	$: currentTitle = title || (mode === 'inspect' ? inspectLabel : workLabel);
	$: currentTab = tabs.find((tab) => tab.id === activeTab);
</script>

<div
	class="flex flex-col gap-1.5 border-b border-gray-200/70 px-2 pt-2 pb-2.5 dark:border-gray-800/80"
>
	<div class="flex items-center gap-3">
		<div class="flex shrink-0 rounded-xl bg-gray-50/70 p-0.5 dark:bg-gray-900/60">
			<button
				type="button"
				class="min-h-9 rounded-lg px-3 py-1.5 text-[13px] transition whitespace-nowrap touch-manipulation focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400/40 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:focus-visible:ring-gray-500/40 dark:focus-visible:ring-offset-gray-950 {mode ===
				'operator'
					? 'bg-gray-100 font-medium text-gray-900 dark:bg-gray-800 dark:text-white'
					: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'}"
				on:click={() => onSetMode('operator')}
			>
				{workLabel}
			</button>
			<button
				type="button"
				class="min-h-9 rounded-lg px-3 py-1.5 text-[13px] transition whitespace-nowrap touch-manipulation focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400/40 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:focus-visible:ring-gray-500/40 dark:focus-visible:ring-offset-gray-950 {mode ===
				'inspect'
					? 'bg-gray-100 font-medium text-gray-900 dark:bg-gray-800 dark:text-white'
					: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'}"
				on:click={() => onSetMode('inspect')}
				disabled={inspectDisabled}
			>
				{inspectLabel}
			</button>
		</div>

		<div class="min-w-0 flex-1">
			<p class="truncate text-sm font-medium text-gray-900 dark:text-white">
				{currentTab?.label || currentTitle}
			</p>
		</div>

		<button
			type="button"
			class="min-h-9 min-w-9 shrink-0 rounded-lg p-2 text-gray-500 transition touch-manipulation hover:bg-gray-100 hover:text-gray-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400/40 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200 dark:focus-visible:ring-gray-500/40 dark:focus-visible:ring-offset-gray-950"
			aria-label={closeLabel}
			on:click={onClose}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.5"
				class="size-4"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
			</svg>
		</button>
	</div>

	<div class="flex items-center gap-1 overflow-x-auto scrollbar-hidden">
		{#each tabs as tab}
			<button
				type="button"
				class="min-h-8 rounded-md px-2.5 py-1.5 text-[12px] leading-4 transition whitespace-nowrap touch-manipulation focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400/40 focus-visible:ring-offset-1 focus-visible:ring-offset-white dark:focus-visible:ring-gray-500/40 dark:focus-visible:ring-offset-gray-950 {activeTab ===
				tab.id
					? 'bg-gray-100 font-medium text-gray-900 dark:bg-gray-800 dark:text-white'
					: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'} {tab.disabled
					? 'cursor-not-allowed opacity-50 hover:text-gray-500 dark:hover:text-gray-400'
					: ''}"
				disabled={tab.disabled}
				on:click={() => onSetTab(tab.id)}
			>
				{tab.label}
			</button>
		{/each}
	</div>
</div>
