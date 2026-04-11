<script lang="ts">
	import { getContext } from 'svelte';

	const i18n = getContext<any>('i18n');

	export let active = false;
	export let history = {};
	export let onJumpToMessage: (message: Record<string, any>) => void = () => {};

	type TodoItem = {
		id: string;
		message: Record<string, any>;
		checked: boolean;
		text: string;
		role: string;
		timestamp: number | null;
	};

	let showCompleted = false;

	const taskLineRegex = /^[\s>*-]*[-*]\s+\[([ xX])\]\s+(.+)$/gm;

	const formatDateTime = (timestamp: number | null | undefined) => {
		if (typeof timestamp !== 'number' || !Number.isFinite(timestamp) || timestamp <= 0) {
			return '';
		}

		return new Intl.DateTimeFormat(undefined, {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(timestamp * 1000));
	};

	const extractTodos = (messages: Record<string, any>): TodoItem[] => {
		if (!messages) return [];

		return (Object.values(messages) as any[]).flatMap((message: any) => {
			if (!message?.content || typeof message.content !== 'string') {
				return [];
			}

			const matches = Array.from(message.content.matchAll(taskLineRegex)) as RegExpMatchArray[];
			return matches.map((match: RegExpMatchArray, index) => ({
				id: `${message.id}-${index}`,
				message,
				checked: match[1].toLowerCase() === 'x',
				text: match[2].trim(),
				role: message.role,
				timestamp:
					typeof message.timestamp === 'number' && Number.isFinite(message.timestamp)
						? message.timestamp
						: null
			}));
		});
	};

	const sortTodos = (items: TodoItem[]) =>
		[...items].sort((left, right) => {
			if (left.checked !== right.checked) {
				return left.checked ? 1 : -1;
			}

			return (right.timestamp ?? 0) - (left.timestamp ?? 0);
		});

	const jumpToMessage = (message: Record<string, any>) => {
		if (!message) {
			return;
		}

		if (onJumpToMessage) {
			onJumpToMessage(message);
			return;
		}

		if (typeof document === 'undefined') {
			return;
		}

		const messageElement = document.getElementById(`message-${String(message.id)}`);
		messageElement?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	};

	let todoItems: TodoItem[] = [];
	let openCount = 0;
	let visibleTodoItems: TodoItem[] = [];

	$: todoItems = sortTodos(extractTodos((history as any)?.messages ?? {}));
	$: openCount = todoItems.filter((item) => !item.checked).length;
	$: visibleTodoItems = showCompleted ? todoItems : todoItems.filter((item) => !item.checked);
</script>

<div class="flex h-full min-h-0 flex-col px-2 py-2">
	<div class="flex items-start justify-between gap-2 px-2 pb-2">
		<div class="min-w-0">
			<div class="text-sm font-medium text-gray-800 dark:text-gray-100">
				{$i18n.t('Action items')}
			</div>
			<div class="mt-0.5 text-[11px] leading-4 text-gray-400 dark:text-gray-500">
				{$i18n.t('Detection is based on markdown checkboxes in chat messages.')}
			</div>
			<div class="mt-1 text-[11px] text-gray-400 dark:text-gray-500">
				{#if showCompleted}
					{$i18n.t('{{COUNT}} items shown', { COUNT: todoItems.length })}
				{:else}
					{$i18n.t('{{COUNT}} open items', { COUNT: openCount })}
				{/if}
			</div>
		</div>

		<button
			type="button"
			class={`inline-flex shrink-0 items-center gap-2 rounded-full border px-2.5 py-1 text-[11px] font-medium transition ${
				showCompleted
					? 'border-gray-200 bg-white text-gray-700 hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-850 dark:text-gray-200 dark:hover:border-gray-600'
					: 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300 hover:bg-white dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200 dark:hover:border-gray-600'
			}`}
			aria-pressed={showCompleted}
			on:click={() => (showCompleted = !showCompleted)}
		>
			<span
				class={`size-1.5 rounded-full ${
					showCompleted ? 'bg-emerald-500' : 'bg-gray-300 dark:bg-gray-600'
				}`}
			></span>
			{#if showCompleted}
				{$i18n.t('Show completed')}
			{:else}
				{$i18n.t('Open only')}
			{/if}
		</button>
	</div>

	<div class="flex-1 min-h-0 overflow-y-auto px-1 pb-2">
		{#if todoItems.length === 0}
			<div class="px-3 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
				{$i18n.t('No checkbox-based action items were found in this chat.')}
			</div>
		{:else if visibleTodoItems.length === 0}
			<div class="px-3 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
				<div class="mx-auto max-w-[18rem] space-y-3">
					<div>{$i18n.t('No open action items are visible.')}</div>
					<button
						type="button"
						class="rounded-full bg-gray-900 px-3 py-1.5 text-[11px] font-medium text-white transition hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100"
						on:click={() => {
							showCompleted = true;
						}}
					>
						{$i18n.t('Show completed')}
					</button>
				</div>
			</div>
		{:else}
			<div class="flex flex-col gap-1">
				{#each visibleTodoItems as item (item.id)}
					<div
						class="rounded-xl border border-gray-100/80 bg-white/80 px-3 py-2.5 dark:border-gray-800/80 dark:bg-gray-900/50"
					>
						<div class="flex items-start gap-2.5">
							<div class="mt-0.5 shrink-0">
								<div
									class="flex size-4 items-center justify-center rounded border border-gray-200 dark:border-gray-700"
								>
									{#if item.checked}
										<div class="size-2 rounded-sm bg-gray-700 dark:bg-gray-200"></div>
									{/if}
								</div>
							</div>

							<div class="min-w-0 flex-1">
								<div
									class={`text-sm leading-6 ${
										item.checked
											? 'text-gray-400 line-through dark:text-gray-500'
											: 'text-gray-800 dark:text-gray-100'
									}`}
								>
									{item.text}
								</div>
								<div
									class="mt-1 flex flex-wrap items-center gap-2 text-[11px] text-gray-400 dark:text-gray-500"
								>
									<span>
										{$i18n.t(
											item.role === 'assistant' ? 'Captured from assistant' : 'Captured from user'
										)}
									</span>
									{#if item.timestamp}
										<span aria-hidden="true">·</span>
										<span>{formatDateTime(item.timestamp)}</span>
									{/if}
									<span aria-hidden="true">·</span>
									<button
										type="button"
										class="font-medium text-gray-500 transition hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
										on:click={() => jumpToMessage(item.message)}
									>
										{$i18n.t('Jump to message')}
									</button>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
