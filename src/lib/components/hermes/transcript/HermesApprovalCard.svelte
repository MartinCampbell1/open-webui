<script lang="ts">
	import { getContext } from 'svelte';
	import { getHermesApprovalSummary } from '$lib/utils/hermesTranscript';

	const i18n = getContext<any>('i18n');

	// TODO(21st): Replace this local approval micro-surface with a 21st.dev-derived pattern once MCP auth is fixed.

	type HermesApprovalResolution = 'once' | 'session' | 'always' | 'deny';
	type HermesApprovalState = {
		title: string;
		description?: string;
		riskLevel?: 'low' | 'medium' | 'high';
		state: 'pending' | 'resolved';
		resolution?: HermesApprovalResolution;
		interactive?: boolean;
	};

	export let approval: HermesApprovalState;
	export let disabled = false;
	export let embedded = false;
	export let onResolve: (resolution: HermesApprovalResolution) => void | Promise<void> = () => {};

	let resolving = false;

	const riskLevelClasses = {
		low: 'border border-emerald-100/70 bg-emerald-50/60 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300',
		medium:
			'border border-amber-100/70 bg-amber-50/60 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300',
		high: 'border border-red-200/70 bg-red-50/70 text-red-800 dark:border-red-500/25 dark:bg-red-500/10 dark:text-red-300'
	};

	const riskLevelLabels = {
		low: () => $i18n.t('Low risk'),
		medium: () => $i18n.t('Needs review'),
		high: () => $i18n.t('High risk')
	};

	$: eyebrowLabel =
		approval?.state === 'resolved' ? $i18n.t('Approval resolved') : $i18n.t('Approval request');

	$: statusLabel =
		approval?.state === 'resolved' && approval?.resolution
			? approval.resolution === 'once'
				? $i18n.t('Allowed once')
				: approval.resolution === 'always'
					? $i18n.t('Allowed always')
					: approval.resolution === 'session'
						? $i18n.t('Allowed for session')
						: $i18n.t('Denied')
			: $i18n.t('Pending approval');
	$: approvalSummary = getHermesApprovalSummary(approval);

	const resolveApproval = async (resolution: HermesApprovalResolution) => {
		if (disabled || resolving) {
			return;
		}

		resolving = true;

		try {
			await onResolve(resolution);
		} finally {
			resolving = false;
		}
	};
</script>

{#if approval}
	<div class={embedded ? 'w-full' : 'mt-2.5 mb-1.5 w-full'}>
		<div
			class={embedded
				? 'rounded-lg border border-gray-100/80 bg-white/80 px-3 py-2.5 dark:border-gray-800/80 dark:bg-gray-950/70'
				: 'rounded-xl border border-gray-100 dark:border-gray-800 bg-gray-50/95 dark:bg-gray-850 px-4 py-3'}
		>
			<div class="flex flex-wrap items-center justify-between gap-2">
				{#if !embedded}
					<div
						class="flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.08em] text-gray-500 dark:text-gray-400"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="1.5"
							class="size-3.5 shrink-0"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 12.75 11.25 15 15 9.75m6 2.25c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9Z"
							/>
						</svg>
						<span>{eyebrowLabel}</span>
					</div>
				{:else}
					<div class="text-[11px] font-medium text-gray-500 dark:text-gray-400">
						{$i18n.t('Approval')}
					</div>
				{/if}

				<div
					class="text-[11px] font-medium rounded-full px-2 py-0.5 bg-white text-gray-600 border border-gray-100 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-800"
				>
					{statusLabel}
				</div>

				{#if approval.state !== 'resolved' && approval.riskLevel}
					<div
						class={`inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.08em] rounded-full px-2 py-0.5 ${
							riskLevelClasses[approval.riskLevel]
						}`}
					>
						{#if approval.riskLevel === 'high'}
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.75"
								class="size-3 shrink-0"
								aria-hidden="true"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M12 9v4m0 4h.01M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h17.94a2 2 0 0 0 1.71-3L14.71 3.86a2 2 0 0 0-3.42 0Z"
								/>
							</svg>
						{/if}
						{riskLevelLabels[approval.riskLevel]()}
					</div>
				{/if}
			</div>

			<div class={embedded ? 'mt-2' : 'mt-2.5'}>
				<div
					class="{embedded
						? 'text-[13px]'
						: 'text-sm'} font-medium text-gray-900 dark:text-gray-100"
				>
					{approval.title}
				</div>

				{#if approval.state !== 'resolved' && approval.description}
					<div class="mt-1 text-[11px] font-medium text-gray-500 dark:text-gray-400">
						{$i18n.t('Pending approval')}
					</div>
				{/if}

				{#if approval.description}
					<div
						class="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-300 whitespace-pre-wrap break-words"
					>
						{approval.description}
					</div>
				{/if}
				{#if approvalSummary}
					<div class="mt-1 text-[11px] text-gray-500 dark:text-gray-400">
						{approvalSummary}
					</div>
				{/if}
			</div>

			{#if approval.state !== 'resolved'}
				{#if !disabled}
					<div class="mt-3 space-y-2 text-sm">
						<div class="flex flex-wrap items-center gap-1.5">
							<button
								type="button"
								disabled={resolving}
								class="{embedded
									? 'px-2.5 py-1'
									: 'px-3 py-1.5'} rounded-3xl bg-gray-900 hover:bg-gray-800 text-gray-100 shadow-sm ring-1 ring-gray-900/10 dark:bg-white dark:hover:bg-gray-100 dark:text-gray-800 dark:ring-white/10 transition font-medium disabled:cursor-not-allowed disabled:opacity-60"
								on:click={() => resolveApproval('once')}
							>
								{$i18n.t('Allow once')}
							</button>
							<button
								type="button"
								disabled={resolving}
								class="{embedded
									? 'px-2.5 py-1'
									: 'px-3 py-1.5'} rounded-3xl bg-white hover:bg-gray-100 text-gray-700 border border-gray-100 dark:bg-gray-900 dark:hover:bg-gray-800 dark:text-gray-200 dark:border-gray-800 transition font-medium disabled:cursor-not-allowed disabled:opacity-60"
								on:click={() => resolveApproval('session')}
							>
								{$i18n.t('Allow for session')}
							</button>
							<button
								type="button"
								disabled={resolving}
								class="{embedded
									? 'px-2.5 py-1'
									: 'px-3 py-1.5'} rounded-3xl border border-red-200/70 bg-red-50/70 hover:bg-red-100 text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:hover:bg-red-500/15 dark:text-red-300 transition font-medium disabled:cursor-not-allowed disabled:opacity-60"
								on:click={() => resolveApproval('deny')}
							>
								{$i18n.t('Deny')}
							</button>
							{#if approval.riskLevel !== 'high'}
								<button
									type="button"
									disabled={resolving}
									class="{embedded
										? 'px-2.5 py-1'
										: 'px-3 py-1.5'} rounded-3xl bg-white hover:bg-gray-100 text-gray-700 border border-gray-100 dark:bg-gray-900 dark:hover:bg-gray-800 dark:text-gray-200 dark:border-gray-800 transition font-medium disabled:cursor-not-allowed disabled:opacity-60"
									on:click={() => resolveApproval('always')}
								>
									{$i18n.t('Allow always')}
								</button>
							{/if}
						</div>

						{#if approval.riskLevel === 'high'}
							<div class="flex flex-wrap items-center gap-1.5">
								<button
									type="button"
									disabled={resolving}
									class="rounded-3xl border border-gray-200/80 bg-white/70 px-2.5 py-1 text-[11px] font-medium text-gray-500 transition hover:bg-gray-100 hover:text-gray-700 dark:border-gray-700 dark:bg-gray-900/70 dark:text-gray-300 dark:hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-60"
									on:click={() => resolveApproval('always')}
								>
									{$i18n.t('Allow always')}
								</button>
							</div>
						{/if}
					</div>
				{/if}
			{:else}
				<div class="mt-2 text-xs text-gray-500 dark:text-gray-400">
					{#if approval.resolution === 'deny'}
						{$i18n.t('This request was declined.')}
					{:else if approval.resolution === 'always'}
						{$i18n.t('This request was approved permanently.')}
					{:else if approval.resolution === 'session'}
						{$i18n.t('This request was approved for the current session.')}
					{:else}
						{$i18n.t('This request was approved.')}
					{/if}
				</div>
			{/if}
		</div>
	</div>
{/if}
