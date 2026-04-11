<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';

	export let history: Record<string, any> = {};
	export let active = false;

	type HermesMessage = Record<string, any> & {
		id?: string;
		parentId?: string | null;
		childrenIds?: string[];
		role?: string;
		timestamp?: number | null;
	};

	const dispatch = createEventDispatcher<{
		open: void;
	}>();
	const i18n = getContext<any>('i18n');

	const getMessages = (value: Record<string, any>) => {
		const rawMessages = value?.messages ?? {};

		if (Array.isArray(rawMessages)) {
			return rawMessages.filter(Boolean) as HermesMessage[];
		}

		if (rawMessages && typeof rawMessages === 'object') {
			return Object.values(rawMessages).filter(Boolean) as HermesMessage[];
		}

		return [];
	};

	const getMessageId = (message: HermesMessage, index: number) =>
		typeof message?.id === 'string' && message.id.trim().length > 0
			? message.id
			: `${message?.role ?? 'message'}-${index}`;

	const getCurrentId = (value: Record<string, any>, messages: HermesMessage[]) => {
		const explicitId =
			typeof value?.currentId === 'string' && value.currentId.trim().length > 0
				? value.currentId
				: typeof value?.current_id === 'string' && value.current_id.trim().length > 0
					? value.current_id
					: null;

		if (
			explicitId &&
			messages.some((message, index) => getMessageId(message, index) === explicitId)
		) {
			return explicitId;
		}

		const lastMessage = messages.at(-1);
		return lastMessage ? getMessageId(lastMessage, messages.length - 1) : null;
	};

	const buildParentMap = (messages: HermesMessage[]) => {
		const messageById = new Map<string, HermesMessage>();
		const childCountById = new Map<string, number>();

		messages.forEach((message, index) => {
			const messageId = getMessageId(message, index);
			messageById.set(messageId, message);
			childCountById.set(messageId, childCountById.get(messageId) ?? 0);
		});

		messages.forEach((message, index) => {
			const messageId = getMessageId(message, index);
			const parentId = typeof message?.parentId === 'string' ? message.parentId : null;

			if (!parentId || !messageById.has(parentId)) {
				return;
			}

			childCountById.set(parentId, (childCountById.get(parentId) ?? 0) + 1);
		});

		return {
			messageById,
			childCountById
		};
	};

	const buildCurrentPath = (currentId: string | null, messageById: Map<string, HermesMessage>) => {
		if (!currentId) {
			return [];
		}

		const trail: HermesMessage[] = [];
		const seen = new Set<string>();
		let cursor: string | null = currentId;

		while (cursor && !seen.has(cursor)) {
			const message = messageById.get(cursor);

			if (!message) {
				break;
			}

			trail.push(message);
			seen.add(cursor);
			cursor = typeof message.parentId === 'string' ? message.parentId : null;
		}

		return trail.reverse();
	};

	let messages: HermesMessage[] = [];
	let currentId: string | null = null;
	let messageById = new Map<string, HermesMessage>();
	let childCountById = new Map<string, number>();
	let currentPath: HermesMessage[] = [];
	let messageCount = 0;
	let branchCount = 0;
	let currentDepth = 0;
	let userTurns = 0;
	let assistantTurns = 0;
	let pathStateLabel = '';
	let activityLabel = '';
	let turnBalanceLabel = '';

	$: messages = getMessages(history);
	$: currentId = getCurrentId(history, messages);
	$: ({ messageById, childCountById } = buildParentMap(messages));
	$: currentPath = buildCurrentPath(currentId, messageById);
	$: messageCount = messages.length;
	$: branchCount = Array.from(childCountById.values()).filter((count) => count > 1).length;
	$: currentDepth = currentPath.length > 0 ? Math.max(currentPath.length - 1, 0) : 0;
	$: userTurns = messages.filter((message) => message?.role === 'user').length;
	$: assistantTurns = messages.filter((message) => message?.role === 'assistant').length;
	$: pathStateLabel =
		currentPath.length > 0
			? currentPath.length === 1
				? $i18n.t('Root path')
				: $i18n.t('Active branch')
			: $i18n.t('No active path');
	$: activityLabel =
		branchCount > 0
			? branchCount === 1
				? $i18n.t('1 branch point')
				: $i18n.t('{{COUNT}} branch points', { COUNT: branchCount })
			: $i18n.t('Linear flow');
	$: turnBalanceLabel = $i18n.t('{{USER_COUNT}} user turns · {{ASSISTANT_COUNT}} assistant turns', {
		USER_COUNT: userTurns,
		ASSISTANT_COUNT: assistantTurns
	});

	const handleOpen = () => {
		dispatch('open');
	};
</script>

<div class="flex h-full min-h-0 flex-col px-2 py-2">
	<div
		class={`flex min-h-0 flex-1 flex-col rounded-xl border px-3 py-3 shadow-sm transition ${
			active
				? 'border-gray-200 bg-white/95 ring-1 ring-gray-900/5 dark:border-gray-700 dark:bg-gray-950/65'
				: 'border-gray-100/80 bg-white/80 dark:border-gray-800/80 dark:bg-gray-950/45'
		}`}
	>
		<div class="flex items-start justify-between gap-3">
			<div class="min-w-0">
				<div
					class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
				>
					{$i18n.t('Overview')}
				</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{$i18n.t('Flow snapshot')}
				</div>
				<div class="mt-1 text-[11px] leading-4 text-gray-500 dark:text-gray-400">
					{$i18n.t('Derived from the current conversation tree.')}
				</div>
			</div>

			<div
				class={`shrink-0 rounded-full border px-2.5 py-1 text-[11px] font-medium ${
					active
						? 'border-gray-200 bg-gray-50 text-gray-700 dark:border-gray-700 dark:bg-gray-900/70 dark:text-gray-200'
						: 'border-gray-100 bg-gray-50/70 text-gray-500 dark:border-gray-800 dark:bg-gray-900/50 dark:text-gray-400'
				}`}
			>
				{pathStateLabel}
			</div>
		</div>

		<div class="mt-3 grid grid-cols-3 gap-2">
			<div
				class="rounded-lg border border-gray-100/80 bg-gray-50/70 px-2.5 py-2 dark:border-gray-800 dark:bg-gray-900/55"
			>
				<div class="text-[11px] text-gray-500 dark:text-gray-400">{$i18n.t('Messages')}</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{messageCount}
				</div>
			</div>
			<div
				class="rounded-lg border border-gray-100/80 bg-gray-50/70 px-2.5 py-2 dark:border-gray-800 dark:bg-gray-900/55"
			>
				<div class="text-[11px] text-gray-500 dark:text-gray-400">{$i18n.t('Branches')}</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{branchCount}
				</div>
			</div>
			<div
				class="rounded-lg border border-gray-100/80 bg-gray-50/70 px-2.5 py-2 dark:border-gray-800 dark:bg-gray-900/55"
			>
				<div class="text-[11px] text-gray-500 dark:text-gray-400">{$i18n.t('Depth')}</div>
				<div class="mt-1 text-sm font-medium text-gray-800 dark:text-gray-100">
					{currentDepth}
				</div>
			</div>
		</div>

		<div
			class="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] leading-4 text-gray-500 dark:text-gray-400"
		>
			<span>{activityLabel}</span>
			<span>{turnBalanceLabel}</span>
		</div>

		<div class="mt-auto pt-3">
			<button
				type="button"
				class="focus-ring touch-target-compact inline-flex w-full items-center justify-center rounded-full bg-gray-900 px-3 py-2 text-[11px] font-medium text-white transition hover:bg-gray-800 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-white"
				on:click={handleOpen}
			>
				{$i18n.t('Open full flow')}
			</button>
		</div>
	</div>
</div>
