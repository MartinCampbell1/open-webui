<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	import {
		getHermesSessionActivityLabel,
		formatHermesSessionSourceLine,
		type HermesSessionListItem
	} from '$lib/utils/hermesSessions';

	const i18n = getContext<any>('i18n');
	const dispatch = createEventDispatcher<{
		open: HermesSessionListItem;
		import: HermesSessionListItem;
		hover: HermesSessionListItem;
	}>();

	export let session: HermesSessionListItem;
	export let busy = false;
	export let selected = false;
	export let showPreview = false;
	export let className = '';

	let mouseOver = false;

	$: activityLabel = getHermesSessionActivityLabel(session.updated_at);
	$: activityText = $i18n.t(activityLabel.key, activityLabel.values ?? {});
	$: sourceLine = formatHermesSessionSourceLine(session);
	$: showExtraDetails = showPreview || selected || mouseOver;
	$: showActionLabel = busy || selected || mouseOver;
	$: sessionStateLabel = session.imported_chat_id
		? $i18n.t('Linked to chat')
		: $i18n.t('Available to attach');
	$: actionLabel = busy
		? session.imported_chat_id
			? `${$i18n.t('Opening')}...`
			: `${$i18n.t('Attaching')}...`
		: session.imported_chat_id
			? $i18n.t('Open linked chat')
			: $i18n.t('Attach and open');
	$: actionPillLabel = busy
		? session.imported_chat_id
			? $i18n.t('Opening')
			: $i18n.t('Attaching')
		: session.imported_chat_id
			? $i18n.t('Open chat')
			: $i18n.t('Attach');

	const handleActivate = () => {
		if (busy) {
			return;
		}

		if (session.imported_chat_id) {
			dispatch('open', session);
			return;
		}

		dispatch('import', session);
	};

	const handleHover = () => {
		mouseOver = true;
		dispatch('hover', session);
	};
</script>

<button
	type="button"
	class="group flex w-full items-start gap-2 rounded-xl px-2.5 py-2 text-left transition hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400/40 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-slate-500/35 dark:focus-visible:ring-offset-gray-950 dark:hover:bg-gray-900/70 {selected
		? 'bg-gray-50 dark:bg-gray-850'
		: ''} {className}"
	on:click={handleActivate}
	on:mouseenter={handleHover}
	on:mouseleave={() => {
		mouseOver = false;
	}}
	on:focus={handleHover}
	on:blur={() => {
		mouseOver = false;
	}}
	disabled={busy}
	aria-label={`${session.title}. ${actionLabel}`}
	data-arrow-selected={selected ? 'true' : undefined}
>
	<div
		class="mt-1 size-2.5 shrink-0 rounded-full bg-gray-300 transition group-hover:bg-gray-400 dark:bg-gray-700 dark:group-hover:bg-gray-500"
	></div>

	<div class="min-w-0 flex flex-1 items-start gap-2">
		<div class="min-w-0 flex-1">
			<div class="flex min-w-0 items-center gap-2">
				<div class="min-w-0 line-clamp-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{session.title}
				</div>

				{#if session.imported_chat_id}
					<div
						class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 text-[11px] text-gray-600 dark:bg-gray-800 dark:text-gray-300"
					>
						{sessionStateLabel}
					</div>
				{/if}

				{#if session.imported_chat_archived}
					<div
						class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 text-[11px] text-gray-600 dark:bg-gray-800 dark:text-gray-300"
					>
						{$i18n.t('Archived')}
					</div>
				{/if}
			</div>

			<div class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400">
				{sessionStateLabel} · {activityText} · {session.message_count}
				{$i18n.t('Messages')}
			</div>

			{#if showExtraDetails}
				{#if session.last_user_content}
					<div class="mt-0.5 line-clamp-1 text-xs leading-5 text-gray-600 dark:text-gray-300">
						{session.last_user_content}
					</div>
				{/if}

				{#if sourceLine}
					<div class="mt-1 text-[11px] text-gray-500 dark:text-gray-400">{sourceLine}</div>
				{/if}
			{/if}
		</div>

		<div class="shrink-0 pt-0.5">
			<div
				class="min-w-[4.75rem] rounded-full bg-gray-100 px-2 py-1 text-center text-[11px] font-medium text-gray-600 transition-opacity dark:bg-gray-800 dark:text-gray-200 {showActionLabel ||
				selected
					? 'opacity-100'
					: 'pointer-events-none opacity-0 group-focus-visible:opacity-100 supports-[hover:none]:opacity-100'} whitespace-nowrap"
			>
				{actionPillLabel}
			</div>
		</div>
	</div>
</button>
