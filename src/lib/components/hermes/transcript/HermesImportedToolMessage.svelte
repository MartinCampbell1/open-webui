<script lang="ts">
	import dayjs from 'dayjs';
	import { getContext } from 'svelte';

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
	$: toolMeta = [
		surfaceSummary.meta,
		message?.timestamp
			? $i18n.t(formatDate(message.timestamp * 1000), {
					LOCALIZED_TIME: dayjs(message.timestamp * 1000).format('LT'),
					LOCALIZED_DATE: dayjs(message.timestamp * 1000).format('L')
				})
			: ''
	]
		.filter(Boolean)
		.join(' • ');
	$: detailsLabel = expanded ? $i18n.t('Hide') : $i18n.t('Details');

	const toggleExpanded = () => {
		if (!detailContent) {
			return;
		}

		expanded = !expanded;
	};
</script>

{#if message}
	<div class="w-full">
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
				class="mt-1.5 ml-7 rounded-lg border border-gray-200/70 bg-white/85 px-3 py-2 text-xs text-gray-600 dark:border-white/8 dark:bg-gray-950/70 dark:text-gray-300"
			>
				<pre class="whitespace-pre-wrap break-words font-mono">{detailContent}</pre>
			</div>
		{/if}
	</div>
{/if}
