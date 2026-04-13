<script lang="ts">
	import { getContext } from 'svelte';
	import HermesImportedToolMessage from '$lib/components/hermes/transcript/HermesImportedToolMessage.svelte';

	const i18n = getContext<any>('i18n');

	export let history: any = {};
	export let messageIds: string[] = [];

	const COLLAPSED_LIMIT = 1;
	let expanded = false;

	$: total = messageIds.length;
	$: hasOverflow = total > COLLAPSED_LIMIT;
	$: visibleMessageIds =
		hasOverflow && !expanded ? messageIds.slice(0, COLLAPSED_LIMIT) : messageIds;
</script>

{#if messageIds.length > 0}
	<div
		class="mt-2 mb-2 rounded-xl border border-gray-100/80 bg-gray-50/78 px-3 py-2 dark:border-gray-800/80 dark:bg-gray-900/45"
	>
		<div class="flex items-center justify-between gap-2">
			<div class="min-w-0">
				<div
					class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
				>
					{$i18n.t('Imported tools')}
				</div>
				<div class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400">
					{total === 1
						? $i18n.t('1 imported tool result')
						: $i18n.t('{{COUNT}} imported tool results', { COUNT: total })}
				</div>
			</div>

			{#if hasOverflow}
				<button
					type="button"
					class="shrink-0 rounded-full bg-gray-100/80 px-2.5 py-1 text-[11px] font-medium text-gray-500 transition hover:bg-gray-200 hover:text-gray-700 dark:bg-white/[0.06] dark:text-gray-300 dark:hover:bg-white/[0.1]"
					on:click={() => {
						expanded = !expanded;
					}}
				>
					{#if expanded}
						{$i18n.t('Collapse')}
					{:else}
						{$i18n.t('Show all')}
					{/if}
				</button>
			{/if}
		</div>

		<div class="mt-1.5 flex flex-col gap-1.5">
			{#each visibleMessageIds as groupedMessageId (groupedMessageId)}
				<HermesImportedToolMessage {history} messageId={groupedMessageId} />
			{/each}
		</div>
	</div>
{/if}
