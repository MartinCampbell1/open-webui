<script lang="ts">
	import dayjs from 'dayjs';
	import { getContext } from 'svelte';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import HermesToolActivityRow from '$lib/components/hermes/transcript/HermesToolActivityRow.svelte';
	import { formatDate } from '$lib/utils';
	import {
		getHermesImportedToolContent,
		getHermesImportedToolName,
		getHermesImportedToolSurfaceSummary
	} from '$lib/utils/hermesTranscript';

	const i18n = getContext<any>('i18n');

	export let history: any = {};
	export let messageId = '';

	let expanded = false;

	$: message = history?.messages?.[messageId] ?? null;
	$: toolName = getHermesImportedToolName(message);
	$: detailContent = getHermesImportedToolContent(message);
	$: surfaceSummary = getHermesImportedToolSurfaceSummary(message, $i18n.t('Completed'));
	$: toolMeta = surfaceSummary.meta;
	$: detailLines = detailContent
		? detailContent
				.split(/\r?\n/)
				.map((line) => line.trim())
				.filter(Boolean)
		: [];
	$: detailPreviewLines = detailLines.slice(0, 3);
	$: detailsLabel = expanded ? $i18n.t('Hide') : $i18n.t('Details');

	const toggleExpanded = () => {
		if (!detailContent) {
			return;
		}

		expanded = !expanded;
	};
</script>

{#if message}
	<div
		class="w-full rounded-xl border border-gray-100/80 bg-gray-50/80 px-3 py-2 dark:border-gray-800/80 dark:bg-gray-900/45"
	>
		<div class="mb-1.5 flex items-center justify-between gap-2 px-0.5">
			<div
				class="min-w-0 text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
			>
				{$i18n.t('Tool')}
			</div>

			{#if message.timestamp}
				<div
					class="shrink-0 text-xs font-medium first-letter:capitalize text-gray-400 transition group-hover:visible dark:text-gray-500"
				>
					<Tooltip content={dayjs(message.timestamp * 1000).format('LLLL')}>
						<span class="line-clamp-1"
							>{$i18n.t(formatDate(message.timestamp * 1000), {
								LOCALIZED_TIME: dayjs(message.timestamp * 1000).format('LT'),
								LOCALIZED_DATE: dayjs(message.timestamp * 1000).format('L')
							})}</span
						>
					</Tooltip>
				</div>
			{/if}
		</div>

		<HermesToolActivityRow
			name={toolName}
			summary={surfaceSummary.summary}
			meta={toolMeta}
			scopeLabel={$i18n.t('Imported tool result')}
			state="done"
			actionLabel={detailContent ? detailsLabel : ''}
			actionAriaLabel={detailContent ? detailsLabel : ''}
			onClick={toggleExpanded}
			onActionClick={toggleExpanded}
		/>

		{#if expanded && detailContent}
			<div
				class="mt-1.5 rounded-lg border border-gray-100/80 bg-white/85 px-3 py-2.5 shadow-sm dark:border-gray-800/80 dark:bg-gray-950/60"
			>
				<div class="flex items-center justify-between gap-2">
					<div
						class="min-w-0 text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
					>
						{$i18n.t('Details')}
					</div>
				</div>

				{#if detailPreviewLines.length > 0}
					<div class="mt-2 space-y-1.5">
						{#each detailPreviewLines as line}
							<div
								class="rounded-md bg-gray-50/90 px-2.5 py-1.5 text-xs leading-5 text-gray-600 dark:bg-gray-900/60 dark:text-gray-300"
							>
								<div class="line-clamp-2 break-words">{line}</div>
							</div>
						{/each}
					</div>
				{/if}

				<div
					class="mt-2 rounded-md border border-dashed border-gray-200/80 bg-gray-50/70 px-2.5 py-2 dark:border-gray-700 dark:bg-gray-900/50"
				>
					<pre
						class="whitespace-pre-wrap break-words font-mono text-[11px] leading-5 text-gray-600 dark:text-gray-300">{detailContent}</pre>
				</div>
			</div>
		{/if}
	</div>
{/if}
