<script lang="ts">
	export let code_executions = [];

	let _code_executions = [];

	$: _code_executions = code_executions.reduce((acc, code_execution) => {
		let error = null;
		let output = null;
		let status = 'PENDING';
		if (code_execution.result) {
			output = code_execution.result.output;
			if (code_execution.result.error) {
				status = 'ERROR';
				error = code_execution.result.error;
			} else {
				status = 'OK';
			}
		}
		acc.push({
			uuid: code_execution.uuid,
			name: code_execution.name,
			code: code_execution.code,
			language: code_execution.language || 'raw',
			status: status,
			error: error,
			output: output
		});
		return acc;
	}, []);

	let selectedCodeExecution = null;
</script>

<!-- TODO: Add code execution modal dialog similar to CitationsModal -->

{#if _code_executions.length > 0}
	<div class="mt-1 mb-2 w-full flex gap-1 items-center flex-wrap">
		{#each _code_executions as code_execution}
			<div class="flex gap-1 text-xs font-semibold">
				<button
					class="flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl max-w-96"
					on:click={() => {
						selectedCodeExecution = code_execution;
						// TODO: Show modal dialog here.
					}}
				>
					<div class="bg-white dark:bg-gray-700 rounded-full size-4">
						{#if code_execution.status == 'OK'}
							&#x2705; <!-- Checkmark -->
						{:else if code_execution.status == 'ERROR'}
							&#x274C; <!-- X mark -->
						{:else if code_execution.status == 'PENDING'}
							&#x23F3; <!-- Hourglass -->
						{:else}
							&#x2049;&#xFE0F; <!-- Interrobang -->
						{/if}
					</div>
					<div class="flex-1 mx-2 line-clamp-1">
						{code_execution.name}
					</div>
				</button>
			</div>
		{/each}
	</div>
{/if}
