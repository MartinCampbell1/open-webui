<script lang="ts">
	import { getContext } from 'svelte';

	const i18n = getContext<any>('i18n');

	// TODO(21st): Replace this local operational grouping pattern with a 21st.dev-derived pattern once MCP auth is fixed.

	export let title = '';
	export let subtitle = '';
	export let meta = '';
	export let busy = false;
	export let tone: 'default' | 'active' | 'warning' = 'default';

	const toneClasses = {
		default: 'border-l-gray-200/80 dark:border-l-gray-700/70',
		active: 'border-l-blue-200/80 dark:border-l-blue-700/60',
		warning: 'border-l-amber-200/90 dark:border-l-amber-600/60'
	};

	$: accentClass = toneClasses[tone] ?? toneClasses.default;
	$: resolvedTitle = title || (busy ? $i18n.t('Agent activity') : $i18n.t('Trust layer'));
</script>

<div
	class={`mt-2.5 mb-1.5 w-full rounded-xl border border-l-2 border-gray-100/80 bg-gray-50/80 px-3 py-2.5 dark:border-gray-800/80 dark:bg-gray-900/50 ${accentClass}`}
>
	<div class="flex items-center justify-between gap-2">
		<div class="min-w-0 flex items-start gap-2">
			<div class="mt-0.5 shrink-0">
				{#if busy}
					<span class="relative flex size-2">
						<span
							class="absolute inline-flex h-full w-full animate-ping rounded-full bg-gray-400/50 dark:bg-gray-500/40"
						></span>
						<span class="relative inline-flex size-2 rounded-full bg-gray-400 dark:bg-gray-500"
						></span>
					</span>
				{:else}
					<span class="inline-flex size-2 rounded-full bg-gray-300 dark:bg-gray-600"></span>
				{/if}
			</div>

			<div class="min-w-0">
				<div
					class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
				>
					{resolvedTitle}
				</div>

				{#if subtitle}
					<div class="mt-0.5 text-[11px] text-gray-400 dark:text-gray-500">
						{subtitle}
					</div>
				{/if}
			</div>
		</div>

		{#if meta}
			<div
				class="shrink-0 rounded-full bg-white/80 px-2 py-0.5 text-[11px] text-gray-400 ring-1 ring-gray-100 dark:bg-gray-950/70 dark:text-gray-500 dark:ring-gray-800"
			>
				{meta}
			</div>
		{/if}
	</div>

	<div class="mt-2 flex flex-col gap-2">
		<slot />
	</div>
</div>
