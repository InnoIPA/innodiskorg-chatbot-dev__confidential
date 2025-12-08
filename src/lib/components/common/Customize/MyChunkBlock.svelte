<script lang="ts">
	import MyCheckbox from '$lib/components/common/Customize/MyCheckbox.svelte';
	import MySwitch from '$lib/components/common/Customize/MySwitch.svelte';
	import { createEventDispatcher } from 'svelte';

	export let chunkItem = {
		imageUrl: null,
		content: null,
		id: null,
		checked: false,
		enabled: false
	};

	let showFullImage = false;

    const tableStyle=`<style>th,td {border: 1px solid slategray;padding: 5px;}table {width:100%;table-layout: fixed;}caption{color:blue;font-size:18px;font-weight:bold}</style>`



	const dispatch = createEventDispatcher();

	const handleToggleCheckbox = (myEvent, myId) => {
		if (myEvent.detail === 'checked') {
			chunkItem.checked = true;
		} else {
			chunkItem.checked = false;
		}

		dispatch('toggleCheckBox', { id: chunkItem.id, checked: chunkItem.checked });
	};

	const handleToggleSwitchButton = (myEvent, myId) => {
		if (myEvent.detail) {
			chunkItem.enabled = true;
		} else {
			chunkItem.enabled = false;
		}
	};
</script>

<style>
	table,
	th,
	td {
		border: 1px solid;
	}
</style>

<div
	class="w-full bg-slate-100 text-black border-gray-500 border-0 mb-3 flex flex-row gap-2 item-top justify-between rounded-lg p-3"
>
	<div class="flex flex-row gap-2">
		<div class="p-0 flex items-top">
			<MyCheckbox
				state={chunkItem.checked ? 'checked' : 'unchecked'}
				on:change={(evt) => handleToggleCheckbox(evt, chunkItem.id)}
			/>
		</div>
		<div class="relative">
			<img
				src={`/${chunkItem.imageUrl}`}
				alt="Chunk Block"
				class="max-w-[100px]"
				on:mouseenter={() => {
					showFullImage = true;
				}}
				on:mouseleave={() => {
					showFullImage = false;
				}}
			/>
			{#if showFullImage}
				<img
					src={`/${chunkItem.imageUrl}`}
					alt="Chunk Block"
					class="max-w-[600px] absolute top-0 left-[100px] border-[3px] border-gray-300 p-2 bg-white"
				/>
			{/if}
		</div>
		<div class="w-full text-[12px]">
			{@html tableStyle + chunkItem.content}
		</div>
	</div>
	<div class="text-sm">
		<MySwitch
			state={chunkItem.enabled}
			on:change={(evt) => handleToggleSwitchButton(evt, chunkItem.id)}
		/>
	</div>
</div>


