<script lang="ts">
	import { getContext } from 'svelte';

	type ContinuityCard = {
		label: string;
		value: string;
		detail?: string;
		present: boolean;
	};

	type PromptSuggestion = {
		label: string;
		prompt: string;
	};

	export let userName = '';
	export let workspaceName = '';
	export let workspaceDetail = '';
	export let profileName = '';
	export let profileDetail = '';
	export let currentRunLabel = '';
	export let currentRunDetail = '';
	export let examplePrompts: PromptSuggestion[] = [];
	export let onPromptSelect: (prompt: string) => void | Promise<void> = () => {};

	const i18n = getContext<any>('i18n');

	$: defaultPrompts = [
		{
			label: $i18n.t('Plan the next Hermes step'),
			prompt: $i18n.t(
				'Help me map the next Hermes step with the current workspace and profile in mind.'
			)
		},
		{
			label: $i18n.t('Summarize the run context'),
			prompt: $i18n.t(
				'Summarize the active Hermes context and point out anything missing before I start.'
			)
		},
		{
			label: $i18n.t('Start a focused Hermes run'),
			prompt: $i18n.t('Start a focused Hermes run and keep it tied to this workspace.')
		},
		{
			label: $i18n.t('Check Hermes continuity'),
			prompt: $i18n.t('Check the workspace, profile, and current Hermes run for continuity gaps.')
		}
	] as PromptSuggestion[];

	$: continuityCards = [
		{
			label: $i18n.t('Workspace'),
			value: workspaceName?.trim() || $i18n.t('No workspace selected'),
			detail:
				workspaceDetail?.trim() ||
				$i18n.t(
					'Use the active Hermes workspace to keep files, outputs, and follow-up work grounded.'
				),
			present: !!workspaceName?.trim()
		},
		{
			label: $i18n.t('Profile'),
			value: profileName?.trim() || $i18n.t('No profile selected'),
			detail:
				profileDetail?.trim() ||
				$i18n.t(
					'The active Hermes profile keeps model, memory, and skills aligned for the next run.'
				),
			present: !!profileName?.trim()
		},
		{
			label: $i18n.t('Live run'),
			value: currentRunLabel?.trim() || $i18n.t('Idle'),
			detail:
				currentRunDetail?.trim() || $i18n.t('Review the live run before you start the next task.'),
			present: !!currentRunLabel?.trim() && currentRunLabel.trim() !== $i18n.t('Idle')
		}
	] as ContinuityCard[];

	$: visiblePrompts = examplePrompts.length > 0 ? examplePrompts : defaultPrompts;
	$: visibleContinuityCards = continuityCards.filter((card) => card.present);

	const handlePromptSelect = async (prompt: string) => {
		if (!prompt) return;

		await onPromptSelect(prompt);
	};
</script>

<div class="flex h-full min-h-0 flex-col px-2 py-2">
	<div
		class="rounded-xl border border-gray-100/80 bg-white/80 px-4 py-4 dark:border-gray-800/80 dark:bg-gray-900/50"
	>
		<div class="max-w-2xl">
			<div
				class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
			>
				{$i18n.t('Hermes entry point')}
			</div>
			<div class="mt-2 text-base font-medium text-gray-800 dark:text-gray-100">
				{#if userName?.trim()}
					{$i18n.t('Welcome back, {{NAME}}', { NAME: userName.trim() })}
				{:else}
					{$i18n.t('Start with the active Hermes context already in view.')}
				{/if}
			</div>
			<div class="mt-2 text-sm leading-6 text-gray-500 dark:text-gray-400">
				{$i18n.t(
					'Hermes keeps this chat, workspace, profile, and live run connected from the first message.'
				)}
			</div>
		</div>

		{#if visibleContinuityCards.length > 0}
			<div
				class={`mt-4 grid gap-2 ${visibleContinuityCards.length > 1 ? 'sm:grid-cols-2' : ''} ${visibleContinuityCards.length > 2 ? 'xl:grid-cols-3' : ''}`}
			>
				{#each visibleContinuityCards as card}
					<div
						class="rounded-xl border border-gray-100 bg-gray-50/80 px-3 py-3 dark:border-gray-800 dark:bg-gray-900/70"
					>
						<div
							class="text-[10px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
						>
							{card.label}
						</div>
						<div class="mt-2 line-clamp-1 text-sm font-medium text-gray-700 dark:text-gray-200">
							{card.value}
						</div>
						<div class="mt-1 text-[11px] leading-4 text-gray-500 dark:text-gray-400">
							{card.detail}
						</div>
					</div>
				{/each}
			</div>
		{/if}

		<div class="mt-4">
			<div
				class="text-[11px] font-medium uppercase tracking-[0.08em] text-gray-400 dark:text-gray-500"
			>
				{$i18n.t('Hermes starter prompts')}
			</div>

			<div class="mt-2 flex flex-wrap gap-2">
				{#each visiblePrompts as prompt}
					<button
						type="button"
						class="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-sm text-gray-600 transition hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800 dark:border-gray-800 dark:bg-gray-950/40 dark:text-gray-300 dark:hover:border-gray-700 dark:hover:bg-gray-900 dark:hover:text-gray-100"
						disabled={!prompt.prompt}
						on:click={() => handlePromptSelect(prompt.prompt)}
					>
						{prompt.label}
					</button>
				{/each}
			</div>
		</div>
	</div>
</div>
