<script lang="ts">
	import { getContext, createEventDispatcher, tick } from 'svelte';
	import { fade } from 'svelte/transition';
	import type { HermesContextSummary } from '$lib/stores';

	const dispatch = createEventDispatcher();

	import { getChatList } from '$lib/apis/chats';

	import { user, selectedFolder, chats, currentChatPage } from '$lib/stores';

	import MessageInput from './MessageInput.svelte';
	import FolderPlaceholder from './Placeholder/FolderPlaceholder.svelte';
	import FolderTitle from './Placeholder/FolderTitle.svelte';
	import HermesSessionConversationSurface from '$lib/components/hermes/context/HermesSessionConversationSurface.svelte';
	import HermesWelcomePanel from '$lib/components/hermes/onboarding/HermesWelcomePanel.svelte';

	const i18n = getContext('i18n');

	export let createMessagePair: Function;
	export let stopResponse: Function;

	export let autoScroll = false;

	export let atSelectedModel: Model | undefined;
	export let selectedModels: [''];

	export let history;

	export let prompt = '';
	export let files = [];
	export let messageInput = null;

	export let selectedToolIds = [];
	export let selectedFilterIds = [];
	export let pendingOAuthTools = [];

	export let showCommands = false;

	export let imageGenerationEnabled = false;
	export let codeInterpreterEnabled = false;
	export let webSearchEnabled = false;

	export let onUpload: Function = (e) => {};
	export let onSelect = (e) => {};
	export let onChange = (e) => {};

	export let toolServers = [];

	export let dragged = false;
	export let hermesContextSummary: HermesContextSummary | null = null;
	export let onOpenHermesControlsTarget: (
		target: 'workspace' | 'profile' | 'context' | 'sessions' | 'tasks'
	) => void = () => {};

	const openComposerHermesControlsTarget = (
		target: 'workspace' | 'profile' | 'context' | 'tasks'
	) => {
		onOpenHermesControlsTarget(target);
	};

	const applyWelcomePrompt = async (nextPrompt: string) => {
		if (!nextPrompt) {
			return;
		}

		prompt = nextPrompt;
		await tick();

		if (messageInput?.setText) {
			await messageInput.setText(nextPrompt);
		}
	};

	$: welcomeWorkspaceName = hermesContextSummary?.workspaceLabel ?? '';
	$: welcomeWorkspaceDetail =
		typeof hermesContextSummary?.generatedFileCount === 'number' &&
		hermesContextSummary.generatedFileCount > 0
			? $i18n.t('{{COUNT}} generated files are already available from the active workspace.', {
					COUNT: hermesContextSummary.generatedFileCount
				})
			: $i18n.t('Use the active workspace to keep files, outputs, and follow-up work grounded.');
	$: welcomeProfileName = hermesContextSummary?.profileLabel ?? '';
	$: welcomeProfileDetail =
		typeof hermesContextSummary?.profileSkillCount === 'number' &&
		hermesContextSummary.profileSkillCount > 0
			? $i18n.t('{{COUNT}} profile skills are ready for the next run.', {
					COUNT: hermesContextSummary.profileSkillCount
				})
			: hermesContextSummary?.profileMemoryEnabled
				? $i18n.t('The active profile keeps memory enabled for follow-up work.')
				: $i18n.t(
						'The active Hermes profile keeps model, memory, and skills aligned for the next run.'
					);
	$: welcomeCurrentRunLabel =
		hermesContextSummary?.activeModelLabel?.trim() ||
		(hermesContextSummary?.sessionStateLabel
			? $i18n.t(hermesContextSummary.sessionStateLabel)
			: $i18n.t('Idle'));
	$: welcomeCurrentRunDetail =
		typeof hermesContextSummary?.taskCount === 'number' && hermesContextSummary.taskCount > 0
			? $i18n.t('{{COUNT}} live tasks are already active in this chat.', {
					COUNT: hermesContextSummary.taskCount
				})
			: typeof hermesContextSummary?.chatAttachedFileCount === 'number' &&
				  hermesContextSummary.chatAttachedFileCount > 0
				? $i18n.t('{{COUNT}} attached files will carry into the next prompt.', {
						COUNT: hermesContextSummary.chatAttachedFileCount
					})
				: $i18n.t('Review the live run before you start the next task.');
	$: showWelcomeContextSurface =
		!!hermesContextSummary &&
		(!!hermesContextSummary.sessionId ||
			!!hermesContextSummary.targetId ||
			(typeof hermesContextSummary.taskCount === 'number' && hermesContextSummary.taskCount > 0));
</script>

<div class="m-auto w-full max-w-6xl px-2 @2xl:px-20 translate-y-6 py-24 text-center">
	<div
		class="w-full text-3xl text-gray-800 dark:text-gray-100 text-center flex items-center gap-4 font-primary"
	>
		<div class="w-full flex flex-col justify-center items-center">
			{#if $selectedFolder}
				<FolderTitle
					folder={$selectedFolder}
					onUpdate={async (folder) => {
						await chats.set(await getChatList(localStorage.token, $currentChatPage));
						currentChatPage.set(1);
					}}
					onDelete={async () => {
						await chats.set(await getChatList(localStorage.token, $currentChatPage));
						currentChatPage.set(1);

						selectedFolder.set(null);
					}}
				/>
			{:else}
				<div class="w-full max-w-4xl px-5">
					<HermesWelcomePanel
						userName={$user?.name ?? ''}
						workspaceName={welcomeWorkspaceName}
						workspaceDetail={welcomeWorkspaceDetail}
						profileName={welcomeProfileName}
						profileDetail={welcomeProfileDetail}
						currentRunLabel={welcomeCurrentRunLabel}
						currentRunDetail={welcomeCurrentRunDetail}
						onPromptSelect={applyWelcomePrompt}
					/>
				</div>

				{#if showWelcomeContextSurface}
					<div class="mt-5 w-full max-w-3xl px-5">
						<HermesSessionConversationSurface
							summary={hermesContextSummary}
							on:context={() => onOpenHermesControlsTarget('context')}
							on:sessions={() => onOpenHermesControlsTarget('sessions')}
							on:workspace={() => onOpenHermesControlsTarget('workspace')}
							on:tasks={() => onOpenHermesControlsTarget('tasks')}
							on:profile={() => onOpenHermesControlsTarget('profile')}
						/>
					</div>
				{/if}
			{/if}

			<div class="text-base font-normal @md:max-w-3xl w-full py-3 {atSelectedModel ? 'mt-2' : ''}">
				<MessageInput
					bind:this={messageInput}
					hermesMode={true}
					{history}
					{selectedModels}
					bind:files
					bind:prompt
					bind:autoScroll
					bind:selectedToolIds
					bind:selectedFilterIds
					bind:imageGenerationEnabled
					bind:codeInterpreterEnabled
					bind:webSearchEnabled
					bind:atSelectedModel
					bind:showCommands
					bind:dragged
					{pendingOAuthTools}
					{toolServers}
					{stopResponse}
					{createMessagePair}
					{hermesContextSummary}
					{onChange}
					onOpenHermesControlsTarget={openComposerHermesControlsTarget}
					{onUpload}
					on:submit={(e) => {
						dispatch('submit', e.detail);
					}}
				/>
			</div>
		</div>
	</div>

	{#if $selectedFolder}
		<div
			class="mx-auto px-4 md:max-w-3xl md:px-6 font-primary min-h-62"
			in:fade={{ duration: 200, delay: 200 }}
		>
			<FolderPlaceholder folder={$selectedFolder} />
		</div>
	{/if}
</div>
