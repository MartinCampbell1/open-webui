<script lang="ts">
	import { Pane, PaneResizer, type PaneAPI } from 'paneforge';
	import { onMount, tick, getContext } from 'svelte';
	import {
		chatControlsOpenTarget,
		config,
		hermesContextLoaded,
		hermesContextLoading,
		hermesProfilesLoaded,
		hermesProfilesLoading,
		hermesProfilesStore,
		hermesRuntimeStore,
		hermesWorkspacesStore,
		terminalServers,
		mobile,
		showControls,
		showCallOverlay,
		showArtifacts,
		showEmbeds,
		settings,
		showFileNavPath,
		selectedTerminalId,
		temporaryChatEnabled,
		user,
		type HermesControlsOpenTarget,
		type WorkspacePanelStatus
	} from '$lib/stores';

	import { uploadFile } from '$lib/apis/files';
	import type { HermesWorkspacesResponse } from '$lib/apis/hermes';
	import { toast } from 'svelte-sonner';
	import { collectHermesGeneratedWorkspaceFiles } from '$lib/utils/hermesWorkspace';
	import { buildHermesContextSummary, ensureHermesContextBundle } from '$lib/utils/hermesContext';

	import Controls from './Controls/Controls.svelte';
	import CallOverlay from './MessageInput/CallOverlay.svelte';
	import Drawer from '../common/Drawer.svelte';
	import Modal from '../common/Modal.svelte';
	import Artifacts from './Artifacts.svelte';
	import Embeds from './ChatControls/Embeds.svelte';
	import HermesControlsModeHeader from './ChatControls/HermesControlsModeHeader.svelte';
	import HermesControlsModeSummary from './ChatControls/HermesControlsModeSummary.svelte';
	import FileNav from './FileNav.svelte';
	import PyodideFileNav from './PyodideFileNav.svelte';
	import Overview from './Overview.svelte';
	import HermesOverviewPanel from '$lib/components/hermes/panels/HermesOverviewPanel.svelte';
	import HermesWorkspaceHeader from '$lib/components/hermes/workspace/HermesWorkspaceHeader.svelte';
	import HermesWorkspaceStub from '$lib/components/hermes/workspace/HermesWorkspaceStub.svelte';
	import HermesSessionPanel from '$lib/components/hermes/panels/HermesSessionPanel.svelte';
	import HermesProfilePanel from '$lib/components/hermes/panels/HermesProfilePanel.svelte';
	import HermesSkillsPanel from '$lib/components/hermes/panels/HermesSkillsPanel.svelte';
	import HermesMemoryPanel from '$lib/components/hermes/panels/HermesMemoryPanel.svelte';
	import HermesTasksPanel from '$lib/components/hermes/panels/HermesTasksPanel.svelte';
	import HermesTodosPanel from '$lib/components/hermes/panels/HermesTodosPanel.svelte';
	import { getResolvedHermesSessionContext } from '$lib/utils/hermesSessions';

	const i18n = getContext<any>('i18n');
	const HERMES_OPERATOR_MODE = true;
	type PanelMode = 'operator' | 'inspect';
	type PanelTabId =
		| 'controls'
		| 'files'
		| 'history'
		| 'overview'
		| 'session'
		| 'profile'
		| 'skills'
		| 'memory'
		| 'tasks'
		| 'todos';
	type PanelTab = {
		id: PanelTabId;
		label: string;
	};

	export let history: Record<string, any> = {};
	export let models: any[] = [];

	export let chatId: string | null = null;
	export let chatHermesSession: Record<string, any> | null = null;
	export let chatMeta: Record<string, any> | null = null;

	export let chatFiles: any[] = [];
	export let params: Record<string, any> = {};

	export let eventTarget: EventTarget;
	export let submitPrompt: Function;
	export let stopResponse: Function;
	export let showMessage: Function;
	export let files: any[] = [];
	export let modelId: string | null = null;
	export let taskIds: string[] | null = null;
	export let generating = false;
	export let pendingApproval: Record<string, any> | null = null;
	export let liveRunActivityMessage: any = null;
	export let liveRunStatusUpdatesEnabled = true;
	export let hermesStreamActive = false;

	export let codeInterpreterEnabled = false;
	export let onHermesProfileSwitched: (
		payload?: Record<string, any> | null
	) => void | Promise<void> = () => {};

	export let pane: PaneAPI | undefined = undefined;

	let largeScreen = false;
	let dragged = false;
	let minSize = 0;
	let paneReady = false;
	let activeMode: PanelMode = 'operator';
	let showOverviewCanvas = false;
	let activeWorkspaceSource: WorkspacePanelStatus['source'] = 'stub';
	let defaultWorkspaceStatus: WorkspacePanelStatus = {
		source: 'stub',
		currentPath: undefined,
		itemCount: undefined,
		visibleItemCount: undefined,
		linkedItemCount: undefined,
		selectedFile: null,
		selectedFileName: null,
		attachEnabled: false
	};
	let effectiveWorkspaceStatus: WorkspacePanelStatus = defaultWorkspaceStatus;

	// Tab state for Controls+Workspace panel
	let activeTab: PanelTabId = 'session';
	let lastControlsContextKey: string | null = null;

	let hasMessages = false;
	let primaryTabs: PanelTab[] = [];
	let inspectTabs: PanelTab[] = [];
	let visibleTabs: PanelTab[] = [];
	let showPrimaryContextSummary = false;
	let showInspectContextSummary = false;
	let derivedPendingApproval: Record<string, any> | null = null;
	let liveRunPendingApproval: Record<string, any> | null = null;
	let liveRunGenerating = false;
	let liveRunActiveModelLabel = '';

	$: hasMessages = !!(history?.messages && Object.keys(history.messages).length > 0);
	$: currentHermesMeta = getResolvedHermesSessionContext({
		session: chatHermesSession,
		meta: chatMeta,
		runtime: $hermesRuntimeStore
	});
	$: controlsContextKey = [
		chatId ?? 'draft',
		currentHermesMeta?.session_id ?? 'no-session',
		currentHermesMeta?.target_id ?? 'no-target'
	].join(':');
	$: showAdvancedTab = HERMES_OPERATOR_MODE
		? $user?.role === 'admin'
		: $user?.role === 'admin' || ($user?.permissions?.chat?.controls ?? true);
	$: showSessionTab = true;
	$: showProfileTab = !!$user;
	$: showSkillsTab = $user?.role === 'admin' || ($user?.permissions?.workspace?.skills ?? false);
	$: showMemoryTab =
		$config?.features?.enable_memories &&
		($user?.role === 'admin' || ($user?.permissions?.features?.memories ?? true));
	$: showTasksTab =
		hasMessages ||
		taskIds !== null ||
		generating ||
		hermesStreamActive ||
		!!pendingApproval ||
		!!derivedPendingApproval;
	$: showTodosTab = hasMessages;
	$: showFilesTab = true;
	$: showOverviewTab = hasMessages;
	$: primaryTabs = [
		...(showSessionTab ? [{ id: 'session', label: $i18n.t('Current context') }] : []),
		...(showSessionTab ? [{ id: 'history', label: $i18n.t('Session history') }] : []),
		...(showFilesTab ? [{ id: 'files', label: $i18n.t('Workspace') }] : []),
		...(showTasksTab ? [{ id: 'tasks', label: $i18n.t('Live run') }] : [])
	] as PanelTab[];
	$: inspectTabs = [
		...(showProfileTab ? [{ id: 'profile', label: $i18n.t('Profile') }] : []),
		...(showSkillsTab ? [{ id: 'skills', label: $i18n.t('Skills') }] : []),
		...(showMemoryTab ? [{ id: 'memory', label: $i18n.t('Memory') }] : []),
		...(showOverviewTab ? [{ id: 'overview', label: $i18n.t('Overview') }] : []),
		...(showTodosTab ? [{ id: 'todos', label: $i18n.t('Todos') }] : []),
		...(showAdvancedTab ? [{ id: 'controls', label: $i18n.t('Advanced') }] : [])
	] as PanelTab[];
	$: visibleTabs = activeMode === 'inspect' ? inspectTabs : primaryTabs;
	$: modeDescription = visibleTabs.map((tab) => tab.label).join(' · ');
	$: showPrimaryContextSummary =
		!!panelContextSummary && activeMode === 'operator' && activeTab === 'tasks';
	$: showInspectContextSummary =
		!!panelContextSummary && activeMode === 'inspect' && activeTab !== 'overview';
	$: if (activeMode === 'inspect' && inspectTabs.length === 0) {
		activeMode = 'operator';
	}
	let workspaceStatus: WorkspacePanelStatus | null = null;

	$: activeWorkspaceSource = $selectedTerminalId
		? 'terminal'
		: codeInterpreterEnabled
			? 'pyodide'
			: 'stub';
	$: generatedWorkspaceFiles = collectHermesGeneratedWorkspaceFiles(history);
	$: stubWorkspaceItemCount = (chatFiles?.length ?? 0) + generatedWorkspaceFiles.length;
	$: defaultWorkspaceStatus = {
		source: activeWorkspaceSource,
		currentPath: undefined,
		itemCount: activeWorkspaceSource === 'stub' ? stubWorkspaceItemCount : undefined,
		visibleItemCount: undefined,
		linkedItemCount: activeWorkspaceSource === 'stub' ? stubWorkspaceItemCount : undefined,
		selectedFile: null,
		selectedFileName: null,
		attachEnabled: false
	} satisfies WorkspacePanelStatus;
	$: effectiveWorkspaceStatus =
		workspaceStatus?.source === activeWorkspaceSource
			? {
					...defaultWorkspaceStatus,
					...workspaceStatus,
					itemCount: workspaceStatus.itemCount ?? defaultWorkspaceStatus.itemCount
				}
			: defaultWorkspaceStatus;
	$: activeHermesWorkspaceItem =
		$hermesWorkspacesStore?.items?.find((item) => item.is_active) ?? null;
	$: activeHermesWorkspaceName = activeHermesWorkspaceItem?.name ?? '';
	$: activeHermesWorkspacePath = activeHermesWorkspaceItem?.path ?? '';
	$: workspaceTitle =
		activeHermesWorkspaceName ||
		($selectedTerminalId
			? $i18n.t('Terminal files')
			: codeInterpreterEnabled
				? $i18n.t('Code workspace')
				: $i18n.t('Workspace'));
	$: workspaceSubtitle = $selectedTerminalId
		? $i18n.t('Browse, preview, and attach files for the current conversation.')
		: codeInterpreterEnabled
			? $i18n.t('Inspect runtime files created during this session.')
			: $i18n.t('Inspect the active Hermes workspace and files attached to this chat.');
	$: workspaceBadge = $selectedTerminalId
		? $i18n.t('Terminal')
		: codeInterpreterEnabled
			? $i18n.t('Local')
			: $i18n.t('Hermes');
	$: workspacePathLabel = effectiveWorkspaceStatus.currentPath
		? $i18n.t('Path: {{PATH}}', { PATH: effectiveWorkspaceStatus.currentPath })
		: activeHermesWorkspacePath
			? $i18n.t('Path: {{PATH}}', { PATH: activeHermesWorkspacePath })
			: activeWorkspaceSource === 'stub'
				? $i18n.t('Chat files only')
				: $i18n.t('No active directory');
	$: workspaceVisibleItemCount =
		typeof effectiveWorkspaceStatus.visibleItemCount === 'number'
			? effectiveWorkspaceStatus.visibleItemCount
			: activeWorkspaceSource !== 'stub' && typeof effectiveWorkspaceStatus.itemCount === 'number'
				? effectiveWorkspaceStatus.itemCount
				: null;
	$: workspaceItemCountLabel =
		typeof workspaceVisibleItemCount === 'number'
			? $i18n.t('Visible items: {{COUNT}}', {
					COUNT: workspaceVisibleItemCount
				})
			: '';
	$: workspaceSelectionLabel = effectiveWorkspaceStatus.selectedFileName
		? $i18n.t('Previewing {{NAME}}', { NAME: effectiveWorkspaceStatus.selectedFileName })
		: '';
	$: workspaceMetaItems = [
		workspacePathLabel,
		workspaceItemCountLabel,
		workspaceSelectionLabel
	].filter(Boolean);
	$: panelContextSummary = buildHermesContextSummary({
		chatHermesSession,
		chatMeta,
		runtime: $hermesRuntimeStore,
		workspaces: $hermesWorkspacesStore,
		profiles: $hermesProfilesStore,
		workspaceStatus: effectiveWorkspaceStatus,
		temporaryChatEnabled: $temporaryChatEnabled,
		currentMessageId: history?.currentId,
		selectedModelLabel: models?.[0]?.name ?? modelId ?? '',
		generatedFileCount: generatedWorkspaceFiles.length,
		chatAttachedFileCount: chatFiles?.length ?? 0,
		taskCount: taskIds?.length ?? 0
	});
	$: liveRunActiveModelLabel =
		panelContextSummary.activeModelLabel ||
		panelContextSummary.browserFallbackModelLabel ||
		models?.[0]?.name ||
		modelId ||
		'';
	$: derivedPendingApproval = (() => {
		const messages = history?.messages ?? {};
		const seen = new Set<string>();
		let messageId = history?.currentId ?? null;

		while (messageId && !seen.has(messageId)) {
			const message = messages[messageId];
			if (!message) {
				break;
			}

			if (message.role === 'assistant' && message?.hermesApproval?.state === 'pending') {
				return message.hermesApproval ?? null;
			}

			seen.add(messageId);
			messageId = message.parentId ?? null;
		}

		return null;
	})();
	$: liveRunPendingApproval = pendingApproval ?? derivedPendingApproval;
	$: liveRunGenerating = generating || hermesStreamActive;
	$: panelStats = [
		typeof panelContextSummary.workspaceVisibleCount === 'number'
			? {
					label: $i18n.t('Workspace'),
					value: panelContextSummary.workspaceVisibleCount
				}
			: null,
		typeof panelContextSummary.chatAttachedFileCount === 'number'
			? {
					label: $i18n.t('Attached'),
					value: panelContextSummary.chatAttachedFileCount
				}
			: null,
		typeof panelContextSummary.generatedFileCount === 'number'
			? {
					label: $i18n.t('Generated'),
					value: panelContextSummary.generatedFileCount
				}
			: null,
		typeof panelContextSummary.taskCount === 'number'
			? {
					label: $i18n.t('Tasks'),
					value: panelContextSummary.taskCount
				}
			: null
	].filter(Boolean);
	$: workspaceHeaderStats = [
		typeof panelContextSummary.workspaceVisibleCount === 'number'
			? {
					label: $i18n.t('Workspace'),
					value: panelContextSummary.workspaceVisibleCount
				}
			: null,
		typeof panelContextSummary.chatAttachedFileCount === 'number'
			? {
					label: $i18n.t('Attached'),
					value: panelContextSummary.chatAttachedFileCount
				}
			: null,
		typeof panelContextSummary.generatedFileCount === 'number'
			? {
					label: $i18n.t('Generated'),
					value: panelContextSummary.generatedFileCount
				}
			: null
	].filter(Boolean);

	const getOperatorFallbackTab = (): PanelTabId => {
		if (showSessionTab) return 'session';
		if (showFilesTab) return 'files';
		if (showTasksTab) return 'tasks';
		if (showProfileTab) return 'profile';
		if (showSkillsTab) return 'skills';
		if (showMemoryTab) return 'memory';
		if (showOverviewTab) return 'overview';
		if (showTodosTab) return 'todos';
		if (showAdvancedTab) return 'controls';
		return 'files';
	};

	const getInspectFallbackTab = (): PanelTabId => {
		if (showProfileTab) return 'profile';
		if (showSkillsTab) return 'skills';
		if (showMemoryTab) return 'memory';
		if (showOverviewTab) return 'overview';
		if (showTodosTab) return 'todos';
		if (showAdvancedTab) return 'controls';
		return getOperatorFallbackTab();
	};

	const isInspectTab = (tabId: PanelTabId): boolean => {
		return inspectTabs.some((tab) => tab.id === tabId);
	};

	const ensureTabForMode = (mode: PanelMode, tabId: PanelTabId): PanelTabId => {
		const tabIsInspect = isInspectTab(tabId);

		if (mode === 'inspect') {
			return tabIsInspect ? tabId : getInspectFallbackTab();
		}

		return tabIsInspect ? getOperatorFallbackTab() : tabId;
	};

	const handleTabSelect = (tabId: string) => {
		activeTab = tabId as PanelTabId;
	};

	const openOperatorTab = (tabId: PanelTabId) => {
		setActiveMode('operator');
		activeTab = tabId;
	};

	const openInspectTab = (tabId: PanelTabId) => {
		setActiveMode('inspect');
		activeTab = tabId;
	};

	const handleControlsClose = () => {
		showOverviewCanvas = false;
		showControls.set(false);
	};

	const handleOpenOverviewCanvas = () => {
		showOverviewCanvas = true;
	};

	const handleCloseOverviewCanvas = () => {
		showOverviewCanvas = false;
	};

	const handleOverviewNodeClick = (e: any) => {
		const node = e?.node;
		const message = node?.data?.message;
		if (!message) {
			return;
		}

		if (node?.data?.message?.favorite) {
			history.messages[node.data.message.id].favorite = true;
		} else if (history?.messages?.[node?.data?.message?.id]) {
			history.messages[node.data.message.id].favorite = null;
		}

		showOverviewCanvas = false;
		showMessage(message, true);
	};

	const setActiveMode = (nextMode: PanelMode) => {
		activeMode = nextMode;
		activeTab = ensureTabForMode(nextMode, activeTab);
	};

	const handleWorkspaceStatusChange = (nextStatus: WorkspacePanelStatus) => {
		workspaceStatus = nextStatus;
	};

	const handleHermesProfileSwitched = async (payload: Record<string, any> | null = null) => {
		hermesRuntimeStore.set(null);
		hermesWorkspacesStore.set(null);
		hermesProfilesStore.set(null);
		hermesContextLoaded.set(false);
		hermesProfilesLoaded.set(false);
		workspaceStatus = null;

		await onHermesProfileSwitched(payload);

		if ($showControls) {
			await ensureHermesContextBundle(localStorage?.token, {
				force: true,
				includeProfiles: true
			});
		}
	};

	const handleHermesWorkspaceSwitched = (payload: HermesWorkspacesResponse) => {
		hermesWorkspacesStore.set(payload);
		hermesContextLoaded.set(true);
		workspaceStatus = null;
	};

	// Tab fallback: if active tab becomes hidden, switch to next available
	$: if (!showOverviewTab && activeTab === 'overview') activeTab = getOperatorFallbackTab();
	$: if (!showSessionTab && activeTab === 'session') activeTab = getOperatorFallbackTab();
	$: if (!showSessionTab && activeTab === 'history') activeTab = getOperatorFallbackTab();
	$: if (!showFilesTab && activeTab === 'files') activeTab = getOperatorFallbackTab();
	$: if (!showSkillsTab && activeTab === 'skills') activeTab = getOperatorFallbackTab();
	$: if (!showMemoryTab && activeTab === 'memory') activeTab = getOperatorFallbackTab();
	$: if (!showTasksTab && activeTab === 'tasks') activeTab = getOperatorFallbackTab();
	$: if (!showTodosTab && activeTab === 'todos') activeTab = getOperatorFallbackTab();
	$: if (!showAdvancedTab && activeTab === 'controls') activeTab = getOperatorFallbackTab();
	$: if (activeMode === 'operator' && isInspectTab(activeTab)) {
		activeTab = getOperatorFallbackTab();
	}
	$: if (activeMode === 'inspect' && !isInspectTab(activeTab) && inspectTabs.length > 0) {
		activeTab = getInspectFallbackTab();
	}
	$: if (controlsContextKey !== lastControlsContextKey) {
		lastControlsContextKey = controlsContextKey;
		workspaceStatus = null;
		showOverviewCanvas = false;
		activeMode = 'operator';
		activeTab = showSessionTab ? 'session' : getOperatorFallbackTab();
	}
	$: if (!$showControls && showOverviewCanvas) {
		showOverviewCanvas = false;
	}

	// Auto-close if there are no visible tabs
	$: if (
		!showAdvancedTab &&
		!showFilesTab &&
		!showOverviewTab &&
		!showSessionTab &&
		!showProfileTab &&
		!showSkillsTab &&
		!showMemoryTab &&
		!showTasksTab &&
		!showTodosTab
	) {
		showControls.set(false);
	}

	$: if ($chatControlsOpenTarget) {
		const openTargetToTab: Record<Exclude<HermesControlsOpenTarget, null>, PanelTabId> = {
			workspace: 'files',
			context: 'session',
			sessions: 'history',
			profile: 'profile',
			tasks: 'tasks'
		};
		const requestedTab = openTargetToTab[$chatControlsOpenTarget];

		if (
			(requestedTab === 'files' && showFilesTab) ||
			(requestedTab === 'session' && showSessionTab) ||
			(requestedTab === 'history' && showSessionTab) ||
			(requestedTab === 'profile' && showProfileTab) ||
			(requestedTab === 'tasks' && showTasksTab)
		) {
			activeTab = requestedTab;
			setActiveMode(isInspectTab(requestedTab) ? 'inspect' : 'operator');
		}

		chatControlsOpenTarget.set(null);
	}

	// Auto-switch to Workspace tab when display_file is triggered
	$: if ($showFileNavPath) {
		activeMode = 'operator';
		activeTab = 'files';
		showControls.set(true);
	}

	$: if ($showControls && (!$hermesContextLoaded || !$hermesProfilesLoaded)) {
		if (!$hermesContextLoading && !$hermesProfilesLoading) {
			void ensureHermesContextBundle(localStorage?.token, { includeProfiles: true });
		}
	}

	// Auto-open Workspace tab when a terminal is selected (suppress panel open when full-screen)
	$: if ($selectedTerminalId) {
		activeMode = 'operator';
		activeTab = 'files';
		if (largeScreen) {
			showControls.set(true);
		}
	}

	// Attach a terminal file to the chat input
	const handleTerminalAttach = async (blob: Blob, name: string, contentType: string) => {
		const tempItemId = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;
		const fileItem = {
			type: 'file',
			file: '',
			id: null,
			url: '',
			name,
			collection_name: '',
			status: 'uploading',
			error: '',
			itemId: tempItemId,
			size: blob.size
		};

		files = [...files, fileItem];

		try {
			const file = new File([blob], name, { type: contentType || 'application/octet-stream' });
			const uploaded = await uploadFile(localStorage.token, file);
			if (!uploaded) throw new Error('Upload failed');

			const idx = files.findIndex((f) => f.itemId === tempItemId);
			if (idx !== -1) {
				files[idx] = {
					...fileItem,
					status: 'uploaded',
					file: uploaded,
					id: uploaded.id,
					url: `${uploaded.id}`,
					collection_name: uploaded?.meta?.collection_name
				};
				files = files;
			}
			toast.success($i18n.t('File attached to chat'));
		} catch (e) {
			files = files.filter((f) => f.itemId !== tempItemId);
			toast.error($i18n.t('Failed to attach file'));
		}
	};

	export const openPane = () => {
		if (!pane) {
			return;
		}

		if (parseInt(localStorage?.chatControlsSize)) {
			const container = document.getElementById('chat-container');
			if (!container?.clientWidth) {
				return;
			}
			let size = Math.floor(
				(parseInt(localStorage?.chatControlsSize) / container.clientWidth) * 100
			);
			pane.resize(size);
		} else {
			pane.resize(minSize);
		}
	};

	const handleMediaQuery = async (e: MediaQueryList | MediaQueryListEvent) => {
		if (e.matches) {
			largeScreen = true;
			if ($showCallOverlay) {
				showCallOverlay.set(false);
				await tick();
				showCallOverlay.set(true);
			}
		} else {
			largeScreen = false;
			if ($showCallOverlay) {
				showCallOverlay.set(false);
				await tick();
				showCallOverlay.set(true);
			}
			pane = undefined;
		}
	};

	const onMouseDown = () => {
		dragged = true;
	};
	const onMouseUp = () => {
		dragged = false;
	};

	onMount(() => {
		const mediaQuery = window.matchMedia('(min-width: 1024px)');
		mediaQuery.addEventListener('change', handleMediaQuery);
		handleMediaQuery(mediaQuery);

		let resizeObserver: ResizeObserver | null = null;
		let isDestroyed = false;

		// Wait for Svelte to render the Pane after largeScreen changed
		const init = async () => {
			await tick();

			if (isDestroyed) return;

			// If controls were persisted as open, set the pane to the saved size
			if ($showControls && pane) {
				openPane();
			}

			setTimeout(() => {
				paneReady = true;
			}, 0);

			const container = document.getElementById('chat-container') as HTMLElement;
			if (!container) return;

			minSize = Math.floor((350 / container.clientWidth) * 100);
			resizeObserver = new ResizeObserver((entries) => {
				for (let entry of entries) {
					const width = entry.contentRect.width;
					minSize = Math.floor((350 / width) * 100);
					if ($showControls) {
						if (pane && pane.isExpanded() && pane.getSize() < minSize) {
							pane.resize(minSize);
						} else {
							let size = Math.floor(
								(parseInt(localStorage?.chatControlsSize) / container.clientWidth) * 100
							);
							if (size < minSize && pane) pane.resize(minSize);
						}
					}
				}
			});
			resizeObserver.observe(container);
		};
		init();

		document.addEventListener('mousedown', onMouseDown);
		document.addEventListener('mouseup', onMouseUp);

		return () => {
			isDestroyed = true;
			paneReady = false;
			resizeObserver?.disconnect();
			if (!largeScreen) {
				showControls.set(false);
			}
			mediaQuery.removeEventListener('change', handleMediaQuery);
			document.removeEventListener('mousedown', onMouseDown);
			document.removeEventListener('mouseup', onMouseUp);
		};
	});

	const closeHandler = () => {
		showOverviewCanvas = false;
		if (!largeScreen) {
			showControls.set(false);
		}
		showArtifacts.set(false);
		showEmbeds.set(false);
		if ($showCallOverlay) showCallOverlay.set(false);
	};

	$: if (
		paneReady &&
		!chatId &&
		activeTab !== 'session' &&
		activeTab !== 'history' &&
		$chatControlsOpenTarget !== 'context' &&
		$chatControlsOpenTarget !== 'sessions'
	) {
		closeHandler();
	}

	// Helper: is a "special" full-screen panel active?
	$: specialPanel = $showCallOverlay || $showArtifacts || $showEmbeds;
</script>

{#if !largeScreen}
	{#if $showControls}
		<Drawer
			show={$showControls}
			onClose={() => showControls.set(false)}
			className="min-h-[100dvh] !bg-white dark:!bg-gray-850"
		>
			<div class="h-[100dvh] flex flex-col">
				{#if $showCallOverlay}
					<div
						class="h-full max-h-[100dvh] bg-white text-gray-700 dark:bg-black dark:text-gray-300 flex justify-center"
					>
						<CallOverlay
							bind:files
							{submitPrompt}
							{stopResponse}
							{modelId}
							{chatId}
							{eventTarget}
							on:close={() => showControls.set(false)}
						/>
					</div>
				{:else if $showEmbeds}
					<Embeds />
				{:else if $showArtifacts}
					<Artifacts />
				{:else}
					<!-- Controls + Workspace tabs -->
					<div class="flex flex-col h-full min-h-0">
						<!-- Tab bar -->
						<HermesControlsModeHeader
							mode={activeMode}
							tabs={visibleTabs}
							{activeTab}
							inspectDisabled={inspectTabs.length === 0}
							closeLabel={$i18n.t('Close')}
							workLabel={$i18n.t('Work')}
							inspectLabel={$i18n.t('Inspect')}
							{modeDescription}
							onSetMode={setActiveMode}
							onSetTab={handleTabSelect}
							onClose={handleControlsClose}
						/>

						<div
							class="flex-1 min-h-0 {activeTab === 'overview'
								? 'overflow-y-auto'
								: activeTab === 'controls'
									? 'overflow-y-auto px-3 pt-1'
									: ''}"
						>
							{#if showPrimaryContextSummary || showInspectContextSummary}
								<HermesControlsModeSummary
									mode={activeMode}
									summary={panelContextSummary}
									stats={panelStats}
									on:workspace={() => openOperatorTab('files')}
									on:session={() => openOperatorTab('session')}
									on:profile={() => openInspectTab('profile')}
								/>
							{/if}

							{#if activeTab === 'overview'}
								<HermesOverviewPanel
									active={activeTab === 'overview'}
									{history}
									on:open={handleOpenOverviewCanvas}
								/>
							{:else if activeTab === 'profile'}
								<HermesProfilePanel
									active={activeTab === 'profile'}
									{taskIds}
									{hermesStreamActive}
									onProfileSwitched={handleHermesProfileSwitched}
								/>
							{:else if activeTab === 'skills'}
								<HermesSkillsPanel active={activeTab === 'skills'} />
							{:else if activeTab === 'memory'}
								<HermesMemoryPanel active={activeTab === 'memory'} />
							{:else if activeTab === 'tasks'}
								<HermesTasksPanel
									active={activeTab === 'tasks'}
									{taskIds}
									{stopResponse}
									generating={liveRunGenerating}
									pendingApproval={liveRunPendingApproval}
									activeModelLabel={liveRunActiveModelLabel}
									activityMessage={liveRunActivityMessage}
									statusUpdatesEnabled={liveRunStatusUpdatesEnabled}
								/>
							{:else if activeTab === 'todos'}
								<HermesTodosPanel
									active={activeTab === 'todos'}
									{history}
									onJumpToMessage={(message: Record<string, any>) => {
										showMessage(message, true);
									}}
								/>
							{:else if activeTab === 'session'}
								<HermesSessionPanel
									active={activeTab === 'session'}
									{chatId}
									{chatHermesSession}
									{chatMeta}
									{history}
									{models}
									{taskIds}
									{chatFiles}
									mode="context"
								/>
							{:else if activeTab === 'history'}
								<HermesSessionPanel
									active={activeTab === 'history'}
									{chatId}
									{chatHermesSession}
									{chatMeta}
									{history}
									{models}
									{taskIds}
									{chatFiles}
									mode="history"
								/>
							{:else if activeTab === 'files' && $selectedTerminalId}
								<div class="flex h-full min-h-0 flex-col">
									<HermesWorkspaceHeader
										title={workspaceTitle}
										subtitle={workspaceSubtitle}
										badge={workspaceBadge}
										metaItems={workspaceMetaItems}
										stats={workspaceHeaderStats}
									/>
									<div class="flex-1 min-h-0">
										<FileNav
											onAttach={handleTerminalAttach}
											onWorkspaceStatusChange={handleWorkspaceStatusChange}
										/>
									</div>
								</div>
							{:else if activeTab === 'files' && codeInterpreterEnabled}
								<div class="flex h-full min-h-0 flex-col">
									<HermesWorkspaceHeader
										title={workspaceTitle}
										subtitle={workspaceSubtitle}
										badge={workspaceBadge}
										metaItems={workspaceMetaItems}
										stats={workspaceHeaderStats}
									/>
									<div class="flex-1 min-h-0">
										<PyodideFileNav
											onAttach={handleTerminalAttach}
											onWorkspaceStatusChange={handleWorkspaceStatusChange}
										/>
									</div>
								</div>
							{:else if activeTab === 'files'}
								<HermesWorkspaceStub
									active={activeTab === 'files'}
									{chatId}
									{chatFiles}
									generatedFiles={generatedWorkspaceFiles}
									{taskIds}
									hermesWorkspaces={$hermesWorkspacesStore?.items ?? []}
									onAttach={handleTerminalAttach}
									onHermesWorkspaceSwitched={handleHermesWorkspaceSwitched}
									onWorkspaceStatusChange={handleWorkspaceStatusChange}
								/>
							{:else}
								<Controls embed={true} {models} bind:chatFiles bind:params />
							{/if}
						</div>
					</div>
				{/if}
			</div>
		</Drawer>
	{/if}
{:else}
	{#if $showControls}
		<PaneResizer
			class="relative flex items-center justify-center group border-l border-gray-50 dark:border-gray-850/30 hover:border-gray-200 dark:hover:border-gray-800 transition z-20"
			id="controls-resizer"
		>
			<div
				class="absolute -left-1.5 -right-1.5 -top-0 -bottom-0 z-20 cursor-col-resize bg-transparent"
			></div>
		</PaneResizer>
	{/if}

	<Pane
		bind:pane
		defaultSize={0}
		onResize={(size) => {
			if ($showControls && pane?.isExpanded()) {
				if (size < minSize) pane.resize(minSize);
				if (size < minSize) {
					localStorage.chatControlsSize = 0;
				} else {
					const container = document.getElementById('chat-container');
					if (container?.clientWidth) {
						localStorage.chatControlsSize = Math.floor((size / 100) * container.clientWidth);
					}
				}
			}
		}}
		onCollapse={() => {
			if (paneReady) showControls.set(false);
		}}
		collapsible={true}
		class="z-10 bg-white dark:bg-gray-850"
	>
		{#if $showControls}
			<div class="flex max-h-full min-h-full">
				<div
					class="w-full {specialPanel && !$showCallOverlay
						? ' '
						: 'bg-white dark:shadow-lg dark:bg-gray-850'} z-40 pointer-events-auto {activeTab ===
					'files'
						? ''
						: 'overflow-y-auto'} scrollbar-hidden"
					id="controls-container"
				>
					{#if $showCallOverlay}
						<div class="w-full h-full flex justify-center">
							<CallOverlay
								bind:files
								{submitPrompt}
								{stopResponse}
								{modelId}
								{chatId}
								{eventTarget}
								on:close={() => showControls.set(false)}
							/>
						</div>
					{:else if $showEmbeds}
						<Embeds overlay={dragged} />
					{:else if $showArtifacts}
						<Artifacts overlay={dragged} />
					{:else}
						<!-- Controls + Workspace tabs -->
						<div class="flex flex-col h-full min-h-0">
							<!-- Tab bar -->
							<HermesControlsModeHeader
								mode={activeMode}
								tabs={visibleTabs}
								{activeTab}
								inspectDisabled={inspectTabs.length === 0}
								closeLabel={$i18n.t('Close')}
								workLabel={$i18n.t('Work')}
								inspectLabel={$i18n.t('Inspect')}
								{modeDescription}
								onSetMode={setActiveMode}
								onSetTab={handleTabSelect}
								onClose={handleControlsClose}
							/>

							<div
								class="flex-1 min-h-0 {activeTab === 'overview'
									? 'overflow-y-auto'
									: activeTab === 'controls'
										? 'overflow-y-auto px-3 pt-1'
										: ''}"
							>
								{#if showPrimaryContextSummary || showInspectContextSummary}
									<HermesControlsModeSummary
										mode={activeMode}
										summary={panelContextSummary}
										stats={panelStats}
										on:workspace={() => openOperatorTab('files')}
										on:session={() => openOperatorTab('session')}
										on:profile={() => openInspectTab('profile')}
									/>
								{/if}

								{#if activeTab === 'overview'}
									<HermesOverviewPanel
										active={activeTab === 'overview'}
										{history}
										on:open={handleOpenOverviewCanvas}
									/>
								{:else if activeTab === 'session'}
									<HermesSessionPanel
										active={activeTab === 'session'}
										{chatId}
										{chatHermesSession}
										{chatMeta}
										{history}
										{models}
										{taskIds}
										{chatFiles}
										mode="context"
									/>
								{:else if activeTab === 'history'}
									<HermesSessionPanel
										active={activeTab === 'history'}
										{chatId}
										{chatHermesSession}
										{chatMeta}
										{history}
										{models}
										{taskIds}
										{chatFiles}
										mode="history"
									/>
								{:else if activeTab === 'profile'}
									<HermesProfilePanel
										active={activeTab === 'profile'}
										{taskIds}
										{hermesStreamActive}
										onProfileSwitched={handleHermesProfileSwitched}
									/>
								{:else if activeTab === 'skills'}
									<HermesSkillsPanel active={activeTab === 'skills'} />
								{:else if activeTab === 'memory'}
									<HermesMemoryPanel active={activeTab === 'memory'} />
								{:else if activeTab === 'tasks'}
									<HermesTasksPanel
										active={activeTab === 'tasks'}
										{taskIds}
										{stopResponse}
										generating={liveRunGenerating}
										pendingApproval={liveRunPendingApproval}
										activeModelLabel={liveRunActiveModelLabel}
										activityMessage={liveRunActivityMessage}
										statusUpdatesEnabled={liveRunStatusUpdatesEnabled}
									/>
								{:else if activeTab === 'todos'}
									<HermesTodosPanel
										active={activeTab === 'todos'}
										{history}
										onJumpToMessage={(message: Record<string, any>) => {
											showMessage(message, true);
										}}
									/>
								{:else if activeTab === 'files' && $selectedTerminalId}
									<div class="flex h-full min-h-0 flex-col">
										<HermesWorkspaceHeader
											title={workspaceTitle}
											subtitle={workspaceSubtitle}
											badge={workspaceBadge}
											metaItems={workspaceMetaItems}
											stats={workspaceHeaderStats}
										/>
										<div class="flex-1 min-h-0">
											<FileNav
												onAttach={handleTerminalAttach}
												onWorkspaceStatusChange={handleWorkspaceStatusChange}
												overlay={dragged}
											/>
										</div>
									</div>
								{:else if activeTab === 'files' && codeInterpreterEnabled}
									<div class="flex h-full min-h-0 flex-col">
										<HermesWorkspaceHeader
											title={workspaceTitle}
											subtitle={workspaceSubtitle}
											badge={workspaceBadge}
											metaItems={workspaceMetaItems}
											stats={workspaceHeaderStats}
										/>
										<div class="flex-1 min-h-0">
											<PyodideFileNav
												onAttach={handleTerminalAttach}
												onWorkspaceStatusChange={handleWorkspaceStatusChange}
												overlay={dragged}
											/>
										</div>
									</div>
								{:else if activeTab === 'files'}
									<HermesWorkspaceStub
										active={activeTab === 'files'}
										{chatId}
										{chatFiles}
										generatedFiles={generatedWorkspaceFiles}
										{taskIds}
										hermesWorkspaces={$hermesWorkspacesStore?.items ?? []}
										onAttach={handleTerminalAttach}
										onHermesWorkspaceSwitched={handleHermesWorkspaceSwitched}
										onWorkspaceStatusChange={handleWorkspaceStatusChange}
									/>
								{:else}
									<Controls embed={true} {models} bind:chatFiles bind:params />
								{/if}
							</div>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</Pane>
{/if}

<Modal
	bind:show={showOverviewCanvas}
	size="2xl"
	containerClassName="p-3 sm:p-5"
	className="overflow-hidden rounded-[1.75rem] bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm"
>
	<div class="flex h-[min(84vh,56rem)] max-h-[84vh] min-h-0 flex-col">
		<div
			class="flex items-center justify-between gap-3 border-b border-gray-200/80 px-4 py-3 dark:border-gray-800/80 sm:px-5"
		>
			<div class="min-w-0">
				<div class="text-sm font-medium text-gray-900 dark:text-white">{$i18n.t('Overview')}</div>
				<div class="mt-0.5 text-xs text-gray-500 dark:text-gray-400">
					{$i18n.t('Open the conversation flow on a wider canvas.')}
				</div>
			</div>

			<button
				type="button"
				class="rounded-lg px-2.5 py-1.5 text-sm text-gray-500 transition hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200"
				on:click={handleCloseOverviewCanvas}
			>
				{$i18n.t('Close')}
			</button>
		</div>

		<div class="min-h-0 flex-1 bg-gray-50/60 p-3 dark:bg-gray-950/40 sm:p-4">
			<div
				class="h-full min-h-0 overflow-hidden rounded-2xl border border-gray-100/80 bg-white/90 dark:border-gray-800/80 dark:bg-gray-900/55"
			>
				<Overview
					{history}
					onNodeClick={handleOverviewNodeClick}
					onClose={handleCloseOverviewCanvas}
				/>
			</div>
		</div>
	</div>
</Modal>
