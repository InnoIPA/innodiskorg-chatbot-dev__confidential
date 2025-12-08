<script lang="ts">
	import { getContext, tick } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { config, models, settings, showCreateChunkModal, user } from '$lib/stores';
	import { updateUserSettings } from '$lib/apis/users';
	import { getModels as _getModels } from '$lib/apis';
	import { goto } from '$app/navigation';

	import Modal from '../common/Modal.svelte';
	import Account from './Settings/Account.svelte';
	import About from './Settings/About.svelte';
	import General from './Settings/General.svelte';
	import Interface from './Settings/Interface.svelte';
	import Audio from './Settings/Audio.svelte';
	import Chats from './Settings/Chats.svelte';
	import User from '../icons/User.svelte';
	import Personalization from './Settings/Personalization.svelte';
	import Search from '../icons/Search.svelte';
	import Connections from './Settings/Connections.svelte';
	import Tools from './Settings/Tools.svelte';
	import { Button } from 'bits-ui';

	import { clickOutside } from '$lib/actions/clickOutside.js';

	const i18n = getContext('i18n');

	export let show = false;

	let keyWordValue = '';
	let keyWordArray = [];
	let questionValue = '';
	let questionArray = [];
	let tagsNum = 0;

	interface SettingsTab {
		id: string;
		title: string;
		keywords: string[];
	}

	const searchData: SettingsTab[] = [
		{
			id: 'general',
			title: 'General',
			keywords: [
				'general',
				'theme',
				'language',
				'notifications',
				'system',
				'systemprompt',
				'prompt',
				'advanced',
				'settings',
				'defaultsettings',
				'configuration',
				'systemsettings',
				'notificationsettings',
				'systempromptconfig',
				'languageoptions',
				'defaultparameters',
				'systemparameters'
			]
		},
		{
			id: 'interface',
			title: 'Interface',
			keywords: [
				'defaultmodel',
				'selectmodel',
				'ui',
				'userinterface',
				'display',
				'layout',
				'design',
				'landingpage',
				'landingpagemode',
				'default',
				'chat',
				'chatbubble',
				'chatui',
				'username',
				'showusername',
				'displayusername',
				'widescreen',
				'widescreenmode',
				'fullscreen',
				'expandmode',
				'chatdirection',
				'lefttoright',
				'ltr',
				'righttoleft',
				'rtl',
				'notifications',
				'toast',
				'toastnotifications',
				'largechunks',
				'streamlargechunks',
				'scroll',
				'scrollonbranchchange',
				'scrollbehavior',
				'richtext',
				'richtextinput',
				'background',
				'chatbackground',
				'chatbackgroundimage',
				'backgroundimage',
				'uploadbackground',
				'resetbackground',
				'titleautogen',
				'titleautogeneration',
				'autotitle',
				'chattags',
				'autochattags',
				'responseautocopy',
				'clipboard',
				'location',
				'userlocation',
				'userlocationaccess',
				'haptic',
				'hapticfeedback',
				'vibration',
				'voice',
				'voicecontrol',
				'voiceinterruption',
				'call',
				'emojis',
				'displayemoji',
				'save',
				'interfaceoptions',
				'interfacecustomization',
				'alwaysonwebsearch'
			]
		},
		{
			id: 'connections',
			title: 'Connections',
			keywords: []
		},
		{
			id: 'tools',
			title: 'Tools',
			keywords: []
		},
		{
			id: 'personalization',
			title: 'Personalization',
			keywords: [
				'personalization',
				'memory',
				'personalize',
				'preferences',
				'profile',
				'personalsettings',
				'customsettings',
				'userpreferences',
				'accountpreferences'
			]
		},
		{
			id: 'audio',
			title: 'Audio',
			keywords: [
				'audio',
				'sound',
				'soundsettings',
				'audiocontrol',
				'volume',
				'speech',
				'speechrecognition',
				'stt',
				'speechtotext',
				'tts',
				'texttospeech',
				'playback',
				'playbackspeed',
				'voiceplayback',
				'speechplayback',
				'audiooutput',
				'speechengine',
				'voicecontrol',
				'audioplayback',
				'transcription',
				'autotranscribe',
				'autosend',
				'speechsettings',
				'audiovoice',
				'voiceoptions',
				'setvoice',
				'nonlocalvoices',
				'savesettings',
				'audioconfig',
				'speechconfig',
				'voicerecognition',
				'speechsynthesis',
				'speechmode',
				'voicespeed',
				'speechrate',
				'speechspeed',
				'audioinput',
				'audiofeatures',
				'voicemodes'
			]
		},
		{
			id: 'chats',
			title: 'Chats',
			keywords: [
				'chat',
				'messages',
				'conversations',
				'chatsettings',
				'history',
				'chathistory',
				'messagehistory',
				'messagearchive',
				'convo',
				'chats',
				'conversationhistory',
				'exportmessages',
				'chatactivity'
			]
		},
		{
			id: 'account',
			title: 'Account',
			keywords: [
				'account',
				'profile',
				'security',
				'privacy',
				'settings',
				'login',
				'useraccount',
				'userdata',
				'api',
				'apikey',
				'userprofile',
				'profiledetails',
				'accountsettings',
				'accountpreferences',
				'securitysettings',
				'privacysettings'
			]
		},
		{
			id: 'admin',
			title: 'Admin',
			keywords: [
				'admin',
				'administrator',
				'adminsettings',
				'adminpanel',
				'systemadmin',
				'administratoraccess',
				'systemcontrol',
				'manage',
				'management',
				'admincontrols',
				'adminfeatures',
				'usercontrol',
				'arenamodel',
				'evaluations',
				'websearch',
				'database',
				'pipelines',
				'images',
				'audio',
				'documents',
				'rag',
				'models',
				'ollama',
				'openai',
				'users'
			]
		},
		{
			id: 'about',
			title: 'About',
			keywords: [
				'about',
				'info',
				'information',
				'version',
				'documentation',
				'help',
				'support',
				'details',
				'aboutus',
				'softwareinfo',
				'timothyjaeryangbaek',
				'openwebui',
				'release',
				'updates',
				'updateinfo',
				'versioninfo',
				'aboutapp',
				'terms',
				'termsandconditions',
				'contact',
				'aboutpage'
			]
		}
	];

	let search = '';
	let visibleTabs = searchData.map((tab) => tab.id);
	let searchDebounceTimeout;

	const searchSettings = (query: string): string[] => {
		const lowerCaseQuery = query.toLowerCase().trim();
		return searchData
			.filter(
				(tab) =>
					tab.title.toLowerCase().includes(lowerCaseQuery) ||
					tab.keywords.some((keyword) => keyword.includes(lowerCaseQuery))
			)
			.map((tab) => tab.id);
	};

	const searchDebounceHandler = () => {
		clearTimeout(searchDebounceTimeout);
		searchDebounceTimeout = setTimeout(() => {
			visibleTabs = searchSettings(search);
			if (visibleTabs.length > 0 && !visibleTabs.includes(selectedTab)) {
				selectedTab = visibleTabs[0];
			}
		}, 100);
	};

	const saveSettings = async (updated) => {
		console.log(updated);
		await settings.set({ ...$settings, ...updated });
		await models.set(await getModels());
		await updateUserSettings(localStorage.token, { ui: $settings });
	};

	const getModels = async () => {
		return await _getModels(
			localStorage.token,
			$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
		);
	};

	let selectedTab = 'general';

	let showKeyWordInput = false;
	let showQuestionInput = false;

	// Function to handle sideways scrolling
	const scrollHandler = (event) => {
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			event.preventDefault(); // Prevent default vertical scrolling
			settingsTabsContainer.scrollLeft += event.deltaY; // Scroll sideways
		}
	};

	const addScrollListener = async () => {
		await tick();
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			settingsTabsContainer.addEventListener('wheel', scrollHandler);
		}
	};

	const removeScrollListener = async () => {
		await tick();
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			settingsTabsContainer.removeEventListener('wheel', scrollHandler);
		}
	};

	$: if (show) {
		addScrollListener();
	} else {
		removeScrollListener();
	}
</script>

<Modal size="md" bind:show>
	<div class="text-gray-700 dark:text-gray-100">
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
			<div class=" text-lg font-medium self-center">Create Chunk</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

		<div class="flex flex-col w-full px-4 pt-1 pb-4 md:space-x-4 gap-1">
			<div class="flex flex-col w-full px-2 py-1 gap-1">
				<div>Chunk</div>
				<div>
					<textarea
						rows="4"
						class="pl-2 pr-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-red-500 w-full"
					/>
				</div>
			</div>
			<div class="flex flex-col w-full px-2 py-1 gap-1">
				<div>Key word</div>
				<div class="h-[30px]">
					{#if !showKeyWordInput}
						<button
							class="bg-gray-100 hover:bg-gray-200 text-white font-bold p-1 flex items-center justify-center rounded w-[36px] h-[32px]"
							on:click={() => {
								showKeyWordInput = true;
							}}
						>
							<svg
								class="w-6 h-6 text-gray-700 dark:text-white"
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
					{:else}
						<input
							type="text"
							bind:value={keyWordValue}
							class="pl-2 pr-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-red-500 w-full"
							use:clickOutside
							on:outclick={(evt) => {
								if (keyWordValue.length > 0) {
									keyWordArray.push(keyWordValue);
									keyWordArray = keyWordArray;
									keyWordValue = '';
								}
								showKeyWordInput = false;
							}}
						/>
					{/if}
				</div>
			</div>

			{#if keyWordArray.length > 0}
				<div class="flex flex-row w-full px-2 py-1 gap-1">
					{#each keyWordArray as item}
						<div
							class="flex flex-row item-center bg-gray-100 h-[30px] rounded-sm px-2 py-1 text-md text-gray-700 mr-2 gap-2"
						>
							{item}
							<button
								class="bg-red-300 hover:bg-red-200 text-white font-bold p-1 flex items-center justify-center rounded w-[24px] h-[24px]"
								on:click={() => {
									keyWordArray = keyWordArray.filter((i) => i !== item);
								}}
							>
								<svg
									class="w-[16px] h-[16px] text-gray-800 dark:text-white"
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
										d="M6 18 17.94 6M18 18 6.06 6"
									/>
								</svg>
							</button>
						</div>
					{/each}
				</div>
			{/if}

			<div class="flex flex-col w-full px-2 py-1 gap-1">
				<div>Question</div>
				<div class="h-[30px]">
					{#if !showQuestionInput}
						<button
							class="bg-gray-100 hover:bg-gray-200 text-white font-bold p-1 flex items-center justify-center rounded w-[36px] h-[32px]"
							on:click={() => {
								showQuestionInput = true;
							}}
						>
							<svg
								class="w-6 h-6 text-gray-700 dark:text-white"
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
					{:else}
						<input
							type="text"
							bind:value={questionValue}
							class="pl-2 pr-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-red-500 w-full"
							use:clickOutside
							on:outclick={() => {
								if (questionValue.length > 0) {
									questionArray.push(questionValue);
									questionArray = questionArray;
									questionValue = '';
								}
								showQuestionInput = false;
							}}
						/>
					{/if}
				</div>
			</div>

			{#if questionArray.length > 0}
				<div class="flex flex-row w-full px-2 py-1 gap-1">
					{#each questionArray as item}
						<div
							class="flex flex-row item-center bg-gray-100 h-[30px] rounded-sm px-2 py-1 text-md text-gray-700 mr-2 gap-2"
						>
							{item}
							<button
								class="bg-red-300 hover:bg-red-200 text-white font-bold p-1 flex items-center justify-center rounded w-[24px] h-[24px]"
								on:click={() => {
									console.log(questionArray);
									questionArray = questionArray.filter((i) => i !== item);
									console.log(questionArray);
								}}
							>
								<svg
									class="w-[16px] h-[16px] text-gray-800 dark:text-white"
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
										d="M6 18 17.94 6M18 18 6.06 6"
									/>
								</svg>
							</button>
						</div>
					{/each}
				</div>
			{/if}

			<div class="flex flex-col w-full px-2 py-1 gap-1">
				<div>Tags</div>

				{#if tagsNum > 0}
					{#each { length: tagsNum } as _, i}
						<div class="flex flex-row w-full px-0 py-1 gap-1 items-center justify-between">
							<select
								class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[300px] p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
							>
								<option value="dog">Dog</option>
								<option value="cat">Cat</option>
								<option value="hamster">Hamster</option>
							</select>
							<input
								type="number"
								class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[300px] p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
								name="tentacles"
								min="10"
								max="100"
							/>
							<button
								class="flex flex-row items-center justify-center px-3 cursor-pointer rounded-md text-gray-500 group"
								on:click={() => {
									tagsNum -= 1;
								}}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="lucide lucide-circle-minus text-red-500"
									aria-hidden="true"
									><circle cx="12" cy="12" r="10"></circle><path d="M8 12h8"></path></svg
								>
							</button>
						</div>
					{/each}
				{/if}

				<div>
					<button
						class="flex items-center justify-center gap-1 px-3 cursor-pointer h-[40px] rounded-md text-[16px] w-full text-gray-500 group hover:bg-gray-200 bg-gray-100 py-1 px-2"
						on:click={() => {
							tagsNum += 1;
						}}
					>
						<svg
							class="w-[18px] h-[18px] text-gray-500 dark:text-white"
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
						Add tag</button
					>
				</div>
			</div>
			<div class="flex flex-row w-full p-2 gap-2 justify-end items-center">
				<button
					class="flex items-center gap-1 px-3 cursor-pointer rounded-md text-[16px] text-gray-500 group hover:text-gray-600 bg-gray-100 py-1 px-2"
					on:click={() => {
						showCreateChunkModal.set(false);
					}}>Cancel</button
				>
				<button
					class="flex items-center gap-1 px-3 cursor-pointer rounded-md text-[16px] text-white group hover:bg-gray-600 bg-black py-1 px-2"
					on:click={() => {}}>Confirm</button
				>
			</div>
		</div>
	</div>
</Modal>

<style>
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		/* display: none; <- Crashes Chrome on hover */
		-webkit-appearance: none;
		margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
	}

	.tabs::-webkit-scrollbar {
		display: none; /* for Chrome, Safari and Opera */
	}

	.tabs {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	input[type='number'] {
		-moz-appearance: textfield; /* Firefox */
	}
</style>
