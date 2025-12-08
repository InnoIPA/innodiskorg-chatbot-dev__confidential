<script>
	import MyCheckbox from '$lib/components/common/Customize/MyCheckbox.svelte';
	import { clickOutside } from '$lib/actions/clickOutside.js';
	import { goto } from '$app/navigation';
	import { knowledgeId, knowledgeFile, showCreateChunkModal } from '$lib/stores';
	import MyChunkBlock from '$lib/components/common/Customize/MyChunkBlock.svelte';
	import MyRadio from '$lib/components/common/Customize/MyRadio.svelte';
	import dayjs from 'dayjs';
	import { PdfViewer } from 'svelte-pdf-simple';
	//	import { content } from 'html2canvas-pro/dist/types/css/property-descriptors/content';

	let _state = 'unchecked';

	let _showPanel = false;

	let _fullText = true;

	let _showOptions = false;

	const hidePanel = () => {
		_showPanel = false;
	};

	let filterOption = 'all';

	let chunkList = [
		{
			id: '1',
			imageUrl: 'ChunkSample_01.jpeg',
			content:
				'<table><tbody><tr><td>Model Name </td><td>M.2 (S42)3IEB</td></tr><tr><td>Flash Type </td><td>iSLC (3D TLC)</td></tr><tr><td>Interface </td><td>SATA III 6.0 Gb/s</td></tr><tr><td>Form Factor </td><td>M.2 2242 B+M Key</td></tr><tr><td>Capacity </td><td>20GB ~320GB</td></tr><tr><td>Sequential R /W (MB/sec, max.)</td><td>550 /500</td></tr><tr><td>P/E Cycle </td><td>100,000</td></tr><tr><td>TBW (Max.)</td><td>20,000</td></tr><tr><td>Storage Temperature </td><td>-40°C ~85°C</td></tr><tr><td>Max. Power Consumption </td><td>1.2W</td></tr><tr><td>Max. Channels </td><td>2</td></tr><tr><td>External DRAM Buffer </td><td>N</td></tr><tr><td>H/W Write Protect </td><td>N</td></tr><tr><td>S.M.A.R.T. </td><td>Y</td></tr><tr><td>AES </td><td>N</td></tr><tr><td>TCG Opal </td><td>N</td></tr><tr><td>Dimension (W x L x H/mm)</td><td>22.0 x 42.0 x 3.5</td></tr><tr><td>Vibration </td><td>20G@[7 ~2000Hz]</td></tr><tr><td>Shock </td><td>1500G@0.5ms</td></tr><tr><td>MTBF </td><td>&gt;3 million hours</td></tr><tr><td>Warranty </td><td>5 Years</td></tr></tbody></table>',
			checked: false,
			enabled: false
		},
		{
			id: '2',
			imageUrl: 'ChunkSample_02.jpeg',
			content:
				'M.2 (S42)3IEBHIGHLIGHT FEATURESUp to 100K P/E cycle, extending the lifespan by 33xEquipped with 112 layer 3D TLC NAND Flash◼tilizes Ultra iSLC Technology◼UiPower Guard &iData Guard supported◼5 year warranty◼SPECIFICATIONS HQ (Taiwan)T +886-2-7703-3000 /E sales@innodisk.com CN T +86-755-2167-3689 /E sales_cn@innodisk.comEU T +31-40-3045-400 /E eusales@innodisk.com US T +1-510-770-9421 /E usasales@innodisk.com JP T +81-3-6667-0161 /E jp_sales@innodisk.com',
			checked: false,
			enabled: false
		},
		{
			id: '3',
			imageUrl: 'ChunkSample_03.jpeg',
			content:
				'1.35(MAX) 1.35(MAX) OF PCB 22.00 Q Q .50 .10 00HO. .00 2 X 10 SEE DETAIL 6.125 ARE 4 5.625 > ARI 20( 10 25 20.0°+5.09 .30±0. 8 (KEEP 0.80±0.08 TOLERANCE: ±O.15mm UNIT: mm DETAIL A SCALE 5:1',
			checked: false,
			enabled: false
		},
		{
			id: '4',
			imageUrl: 'ChunkSample_04.jpeg',
			content:
				'<table><caption>ORDER INFO.</caption><tbody><tr><td>O </td><td>S G 0°C ~70°C </td><td>I G 40°C ~85°C</td></tr><tr><td>20GB </td><td>DHM24-20GIC1KCASL </td><td>DHM24-20GIC1KWASL</td></tr><tr><td>40GB </td><td>DHM24-40GIC1KCADL </td><td>DHM24-40GIC1KWADL</td></tr><tr><td>80GB </td><td>DHM24-80GIC1KCADL </td><td>DHM24-80GIC1KWADL</td></tr><tr><td>160GB </td><td>DHM24-A60IC1KCADL </td><td>DHM24-A60IC1KWADL</td></tr><tr><td>320GB </td><td>DHM24-D2GIC1KCADL </td><td>DHM24-D2GIC1KWADL </td></tr></tbody></table>',
			checked: false,
			enabled: false
		}
	];

	let chunkListFilter = chunkList;

	$: {
		if (filterOption === 'all') chunkListFilter = chunkList;
		if (filterOption === 'enabled')
			chunkListFilter = chunkList.filter((item) => item.enabled === true);
		if (filterOption === 'disabled')
			chunkListFilter = chunkList.filter((item) => item.enabled === false);
		//chunkListFilter= chunkList;
	}

	let checkAll = 'unchecked';

	const parseCheckAll = () => {
		checkAll = chunkList.every((item) => item.checked === true)
			? 'checked'
			: chunkList.every((item) => item.checked === false)
				? 'unchecked'
				: 'indeterminate';
	};

	const handleToggleCheckbox = (myEvent) => {
		parseCheckAll();
	};

	const handleToggleAllCheckbox = (myEvent) => {
		if (myEvent) {
			chunkList = chunkList.map((item) => {
				return {
					...item,
					checked: myEvent === 'checked' ? true : false
				};
			});
		} else {
			chunkList = chunkList.map((item) => {
				return {
					...item,
					checked: checkAll === 'unchecked' ? true : false
				};
			});
		}

		parseCheckAll();
	};

	const handleToggleAllToggleButton = (myEvent) => {
		chunkList = chunkList.map((item) => {
			return {
				...item,
				enabled: item.checked ? myEvent : item.enabled
			};
		});
		parseCheckAll();
	};

	const changeFilterOption = (option) => {
		console.log('changeFilterOption', option);
		filterOption = option;
		_showPanel = false;
	};

	let totalPages = 0;

	const handleLoadedSuccess = (event) => {
		// The event.detail object contains information about the loaded PDF
		totalPages = event.detail.totalPages;
		// You can now use totalPages in your Svelte component
		console.log('totalPages', totalPages);
	};

	const range = (start, end) => {
		const result = [];
		for (let i = start; i <= end; i++) {
			result.push(i);
		}
		return result;
	};

	const options = [
		{
			value: 'all',
			label: 'All'
		},
		{
			value: 'enabled',
			label: 'Enabled'
		},
		{
			value: 'disabled',
			label: 'Disabled'
		}
	];
</script>

<div class="grid grid-cols-2 gap-4 h-full">
	<div class="w-full h-full">
		<div class="h-[40px] text-[20px] flex justify-start items-center gap-2">
			<button
				class="bg-gray-100 hover:bg-gray-200 text-white font-bold p-1 flex items-center justify-center rounded w-[36px] h-[32px]"
				on:click={() => {
					//_showPanel = !_showPanel;
					goto(`/workspace/knowledge/${$knowledgeId}`);
				}}
			>
				<svg
					class="w-6 h-6 text-gray-800 dark:text-white"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					fill="none"
					viewBox="0 0 24 24"
				>
					<path
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M16 16.881V7.119a1 1 0 0 0-1.636-.772l-5.927 4.881a1 1 0 0 0 0 1.544l5.927 4.88a1 1 0 0 0 1.636-.77Z"
					/>
				</svg>
			</button>
			<div class="h-[40px] pt-1 pb-0 text-[20px]">{$knowledgeFile.filename}</div>
		</div>
		<div class="h-[30px] pt-0 pb-0 text-[14px] text-gray-500 flex flex-row gap-2">
			<div class="flex flex-row">
				<div class="text-blue-500 font-bold">Size：</div>
				{$knowledgeFile.meta.size}
			</div>
			<!-- Uploaded Time：{ new Date($knowledgeFile.created_at*1000).toISOString() }  <br/> -->
			<div class="flex flex-row">
				<div class="text-blue-500 font-bold">Created Time：</div>
				{dayjs($knowledgeFile.updated_at * 1000).format('YYYY-MM-DD HH:mm:ss')}
			</div>
		</div>

		<div
			class="border border-0 bg-white p-3 shadow-lg text-[30px] text-white shadow-cyan-500/50 rounded-lg shadow-md border-solid pt-0 pb-2 h-[calc(100dvh-180px)] overflow-y-scroll scrollbar-thin scrollbar-track-gray-200 scrollbar-thumb-blue-500 gap-1"
		>
			<PdfViewer
				props={{ url: '/innodisk_m2_s42_3ieb_datasheet.pdf', page: 1 }}
				style="border: 1px solid black; display: block; margin-top: 10px;"
				on:load_success={handleLoadedSuccess}
			/>

			{#if totalPages > 1}
				{#each range(2, totalPages) as i}
					<PdfViewer
						props={{ url: '/innodisk_m2_s42_3ieb_datasheet.pdf', page: i }}
						style="border: 1px solid black; display: block; margin-top: 10px;"
					/>
				{/each}
			{/if}
		</div>
	</div>

	<div class="w-full h-full flex flex-col gap-2">
		<div class="h-[40px] text-[20px]">Chunk Result</div>
		<div class="h-[30px] text-[14px] text-gray-500">
			View the chunked segments used for embedding and retrieval. aaa.
		</div>
		<div class="h-[32px] text-[14px] flex justify-between">
			<div class="flex flex-row gap-0">
				<button
					class="bg-gray-200 hover:bg-gray-100 text-white font-bold py-1 px-2 rounded-tl-md rounded-bl-md w-[80px]"
					on:click={() => {
						_fullText = true;
					}}><span class={_fullText ? 'text-gray-500' : 'text-white'}>Full Text</span></button
				>
				<button
					class="bg-gray-200 hover:bg-gray-100 text-white font-bold py-1 px-2 rounded-tr-md rounded-br-md w-[80px]"
					on:click={() => {
						_fullText = false;
					}}><span class={_fullText ? 'text-white' : 'text-gray-500'}>Ellipse</span></button
				>
			</div>
			<div class="flex flex-row gap-2">
				<div class="relative">
					<input
						type="text"
						placeholder="Search"
						class="pl-10 pr-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-red-500 w-full h-[34px]"
					/>
					<div
						class="absolute inset-y-0 left-[-5px] top-[2px] pl-3 flex items-center pointer-events-none"
					>
						<!-- Your SVG icon code here -->
						<svg
							class="w-6 h-6 text-gray-800 dark:text-white"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="none"
							viewBox="0 0 24 24"
						>
							<path
								stroke="currentColor"
								stroke-linecap="round"
								stroke-width="2"
								d="m21 21-3.5-3.5M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
							/>
						</svg>
					</div>
				</div>

				<div class="relative" use:clickOutside on:outclick={hidePanel}>
					<button
						class="bg-gray-100 hover:bg-gray-200 text-white font-bold p-1 flex items-center justify-center rounded w-[36px] h-[32px]"
						on:click={() => {
							_showPanel = !_showPanel;
						}}
					>
						<svg
							class="w-6 h-6 text-gray-800 dark:text-white"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="none"
							viewBox="0 0 24 24"
						>
							<path
								stroke="currentColor"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M7.119 8h9.762a1 1 0 0 1 .772 1.636l-4.881 5.927a1 1 0 0 1-1.544 0l-4.88-5.927A1 1 0 0 1 7.118 8Z"
							/>
						</svg>
					</button>
					{#if _showPanel}
						<div
							class="flex flex-col gap-1 z-10 absolute top-[34px] left-[-70px] w-[160px] bg-white p-4 rounded-md border border-gray-300 shadow-md"
						>
							<MyRadio {options} fontSize={16} bind:userSelected={filterOption}></MyRadio>
						</div>
					{/if}
				</div>
				<button
					class="bg-gray-100 hover:bg-gray-200 text-white font-bold p-1 flex items-center justify-center rounded w-[36px] h-[32px]"
					on:click={() => {
						showCreateChunkModal.set(true);
					}}
				>
					<svg
						class="w-6 h-6 text-gray-800 dark:text-white"
						aria-hidden="true"
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke="currentColor"
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M5 12h14m-7 7V5"
						/>
					</svg>
				</button>
			</div>
		</div>

		<div class="h-[30px] text-[20px]">
			<div class=" flex items-center gap-3 mr-3 justify-start">
				<div
					class="flex items-center gap-1 cursor-pointer rounded-lg text-[16px] text-gray-500 group hover:text-gray-600 bg-gray-100 py-1 px-2"
				>
					<MyCheckbox
						state={checkAll}
						on:change={(e) => {
							handleToggleAllCheckbox(e.detail);
						}}
					/>
					<span
						on:click={(e) => {
							handleToggleAllCheckbox(null);
						}}>Select All</span
					>
				</div>

				{#if checkAll !== 'unchecked'}
					<div
						class="flex items-center gap-1 cursor-pointer rounded-lg text-[16px] text-gray-500 group hover:text-gray-600 bg-gray-100 py-1 px-2"
						on:click={() => {
							handleToggleAllToggleButton(true);
						}}
					>
						<svg
							class="w-6 h-6 text-gray-800 dark:text-white"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="none"
							viewBox="0 0 24 24"
						>
							<path
								class="stroke-gray-400 group-hover:stroke-gray-600"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
							/>
						</svg>
						<span>Enable</span>
					</div>
				{/if}

				{#if checkAll !== 'unchecked'}
					<div
						class="flex items-center gap-1 cursor-pointer rounded-lg text-[16px] text-gray-500 group hover:text-gray-600 bg-gray-100 py-1 px-2"
						on:click={() => {
							handleToggleAllToggleButton(false);
						}}
					>
						<svg
							class="w-6 h-6 text-gray-800 dark:text-white"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="none"
							viewBox="0 0 24 24"
						>
							<path
								class="stroke-gray-400 group-hover:stroke-gray-600"
								stroke-linecap="round"
								stroke-width="2"
								d="m6 6 12 12m3-6a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
							/>
						</svg>
						<span>Disable</span>
					</div>
				{/if}

				{#if checkAll !== 'unchecked'}
					<div
						class="flex items-center gap-1 cursor-pointer rounded-lg text-[16px] text-red-400 group hover:text-red-600 bg-gray-100 py-1 px-2"
					>
						<svg
							class="w-6 h-6 text-gray-800 dark:text-white"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="none"
							viewBox="0 0 24 24"
						>
							<path
								class="stroke-red-400 group-hover:stroke-red-600"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"
							/>
						</svg>
						<span>Delete</span>
					</div>
				{/if}
			</div>
		</div>
		<div
			class="border border-0 bg-white p-2 shadow-lg text-[30px] text-white shadow-cyan-500/50 rounded-lg shadow-md border-solid h-[calc(100dvh-270px)] overflow-y-scroll scrollbar-thin scrollbar-track-gray-200 scrollbar-thumb-blue-500 gap-1"
		>
			{#each chunkListFilter as chunk}
				<MyChunkBlock chunkItem={chunk} on:toggleCheckBox={handleToggleCheckbox} />
			{/each}
		</div>
	</div>
</div>
