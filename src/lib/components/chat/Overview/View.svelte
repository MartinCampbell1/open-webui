<script lang="ts">
	import { getContext, onDestroy, onMount, tick } from 'svelte';
	import { useSvelteFlow, useNodesInitialized, useStore } from '@xyflow/svelte';
	import { writable } from 'svelte/store';
	import { models, user } from '$lib/stores';

	import '@xyflow/svelte/dist/style.css';

	import CustomNode from './Node.svelte';
	import Flow from './Flow.svelte';

	const i18n = getContext<any>('i18n');
	const { width, height } = useStore();
	const { fitView } = useSvelteFlow();
	const nodesInitialized = useNodesInitialized();

	export let history;
	export let onClose;
	export let onNodeClick;

	const MAX_AUTO_RENDER_MESSAGES = 80;
	const nodes = writable([]);
	const edges = writable([]);
	const nodeTypes = {
		custom: CustomNode
	};

	let selectedMessageId: string | null = null;
	let layoutDirection: 'vertical' | 'horizontal' = 'vertical';
	let mapReady = false;
	let historySignature = '';
	let flowReady = false;
	let fitFrame = 0;

	let unsubscribeNodesInitialized = () => {};
	let unsubscribeWidth = () => {};
	let unsubscribeHeight = () => {};

	$: messageEntries = history?.messages
		? Object.entries(history.messages).filter(([, message]) => !!message)
		: [];
	$: messageIds = messageEntries.map(([id]) => id);
	$: messageCount = messageIds.length;
	$: nextHistorySignature =
		messageCount > 0
			? `${history?.currentId ?? ''}:${messageIds[0]}:${messageIds[messageIds.length - 1]}:${messageCount}`
			: 'empty';

	$: if (nextHistorySignature !== historySignature) {
		historySignature = nextHistorySignature;
		selectedMessageId = null;
		mapReady = messageCount > 0 && messageCount <= MAX_AUTO_RENDER_MESSAGES;
		nodes.set([]);
		edges.set([]);
	}

	$: if (history && mapReady) {
		void drawFlow(layoutDirection);
	}

	$: if (history?.currentId && mapReady && flowReady) {
		void scheduleFitView(selectedMessageId ?? history.currentId);
	}

	const getActivePathIds = (currentId: string | null | undefined) => {
		const activePathIds = new Set<string>();
		let pointer = currentId ?? null;

		while (pointer && history?.messages?.[pointer] && !activePathIds.has(pointer)) {
			activePathIds.add(pointer);
			pointer = history.messages[pointer]?.parentId ?? null;
		}

		return activePathIds;
	};

	const drawFlow = async (direction: 'vertical' | 'horizontal') => {
		if (!history?.messages || !messageEntries.length) {
			nodes.set([]);
			edges.set([]);
			return;
		}

		const nodeList = [];
		const edgeList = [];
		const levelOffset = direction === 'vertical' ? 150 : 300;
		const siblingOffset = direction === 'vertical' ? 250 : 150;
		const positionMap = new Map<string, { id: string; level: number; position: number }>();
		const layerWidths: Record<number, number> = {};
		const activePathIds = getActivePathIds(history.currentId);
		const modelMap = new Map(($models ?? []).map((model) => [model.id, model]));

		for (const [id, message] of messageEntries) {
			const level = message.parentId ? (positionMap.get(message.parentId)?.level ?? -1) + 1 : 0;
			layerWidths[level] = layerWidths[level] ?? 0;

			positionMap.set(id, {
				id: message.id,
				level,
				position: layerWidths[level]++
			});
		}

		for (const [id, message] of messageEntries) {
			const position = positionMap.get(id);
			if (!position) {
				continue;
			}

			const x =
				direction === 'vertical' ? position.position * siblingOffset : position.level * levelOffset;
			const y =
				direction === 'vertical' ? position.level * levelOffset : position.position * siblingOffset;

			nodeList.push({
				id: position.id,
				type: 'custom',
				data: {
					user: $user,
					message,
					model: modelMap.get(message.model)
				},
				position: { x, y }
			});

			if (message.parentId) {
				edgeList.push({
					id: `${message.parentId}-${position.id}`,
					source: message.parentId,
					target: position.id,
					selectable: false,
					class: 'dark:fill-gray-300 fill-gray-300',
					type: 'smoothstep',
					animated: activePathIds.has(id)
				});
			}
		}

		nodes.set(nodeList);
		edges.set(edgeList);
	};

	const scheduleFitView = async (targetId: string | null) => {
		if (!targetId || !flowReady || typeof window === 'undefined') {
			return;
		}

		await tick();

		if (fitFrame) {
			window.cancelAnimationFrame(fitFrame);
		}

		fitFrame = window.requestAnimationFrame(() => {
			void fitView({
				nodes: [{ id: targetId }],
				padding: 0.2,
				duration: 220
			});

			if (selectedMessageId === targetId) {
				selectedMessageId = null;
			}
		});
	};

	const setLayoutDirection = (direction: 'vertical' | 'horizontal') => {
		layoutDirection = direction;
		if (mapReady) {
			void drawFlow(layoutDirection);
		}
	};

	const loadMap = () => {
		mapReady = true;
	};

	onMount(() => {
		unsubscribeNodesInitialized = nodesInitialized.subscribe((initialized) => {
			flowReady = initialized;

			if (initialized && mapReady && history?.currentId) {
				void scheduleFitView(selectedMessageId ?? history.currentId);
			}
		});

		unsubscribeWidth = width.subscribe((value) => {
			if (value && mapReady && flowReady && history?.currentId) {
				void scheduleFitView(selectedMessageId ?? history.currentId);
			}
		});

		unsubscribeHeight = height.subscribe((value) => {
			if (value && mapReady && flowReady && history?.currentId) {
				void scheduleFitView(selectedMessageId ?? history.currentId);
			}
		});
	});

	onDestroy(() => {
		unsubscribeNodesInitialized();
		unsubscribeWidth();
		unsubscribeHeight();

		if (fitFrame && typeof window !== 'undefined') {
			window.cancelAnimationFrame(fitFrame);
		}

		nodes.set([]);
		edges.set([]);
	});
</script>

<div class="flex h-full min-h-0 flex-col">
	{#if messageCount === 0}
		<div
			class="m-3 flex flex-1 min-h-0 items-center justify-center rounded-xl border border-dashed border-gray-200/80 bg-gray-50/70 px-4 py-4 text-center text-xs text-gray-500 dark:border-gray-800 dark:bg-gray-900/30 dark:text-gray-400"
		>
			{$i18n.t('Conversation map will appear once this chat has messages to connect.')}
		</div>
	{:else if !mapReady}
		<div
			class="m-3 flex flex-1 min-h-0 flex-col justify-center rounded-xl border border-gray-100/80 bg-white/85 px-4 py-4 dark:border-gray-800/80 dark:bg-gray-900/45"
		>
			<div
				class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
			>
				{$i18n.t('Conversation map')}
			</div>
			<div class="mt-2 text-sm font-medium text-gray-800 dark:text-gray-100">
				{$i18n.t('Load this map on demand')}
			</div>
			<div class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400">
				{$i18n.t(
					'This chat already has {{COUNT}} messages. The full node graph stays deferred so the side panel does not stall on long histories.',
					{ COUNT: messageCount }
				)}
			</div>
			<div class="mt-3 flex flex-wrap gap-2">
				<button
					class="rounded-full bg-gray-900 px-3 py-1.5 text-[11px] font-medium text-white transition hover:bg-black dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100"
					on:click={loadMap}
				>
					{$i18n.t('Load full map')}
				</button>
				<button
					class="rounded-full bg-gray-100 px-3 py-1.5 text-[11px] font-medium text-gray-600 transition hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
					on:click={onClose}
				>
					{$i18n.t('Close panel')}
				</button>
			</div>
		</div>
	{:else if $nodes.length > 0}
		<div class="min-h-0 flex-1">
			<Flow
				{nodes}
				{nodeTypes}
				{edges}
				{setLayoutDirection}
				on:nodeclick={(event) => {
					onNodeClick(event.detail);
					selectedMessageId = event.detail.node.data.message.id;
					void scheduleFitView(selectedMessageId);
				}}
			/>
		</div>
	{/if}
</div>
