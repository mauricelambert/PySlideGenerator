let slide_index = 0;

document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("main section");

  const scrollToSlide = (index) => {
    if (index >= 0 && index < sections.length) {
      sections[index].scrollIntoView({ behavior: 'smooth' });
      slide_index = index;
    }
  };

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || e.key === "ArrowRight") {
      scrollToSlide(slide_index + 1);
    } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
      scrollToSlide(slide_index - 1);
    }
  });

  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Toggle Theme";
  toggleBtn.className = "theme-toggle";
  document.body.appendChild(toggleBtn);

  const applyTheme = (theme) => {
    document.body.classList.remove("dark", "light");
    document.body.classList.add(theme);
    localStorage.setItem("theme", theme);
  };

  const savedTheme = localStorage.getItem("theme");
  applyTheme(savedTheme || "dark");

  toggleBtn.addEventListener("click", () => {
    const newTheme = document.body.classList.contains("dark") ? "light" : "dark";
    applyTheme(newTheme);
  });

  let scrollTimeout;
  document.querySelector("main").addEventListener("scroll", () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      let closest = 0;
      let minDiff = Infinity;
      sections.forEach((sec, i) => {
        const diff = Math.abs(sec.getBoundingClientRect().top);
        if (diff < minDiff) {
          minDiff = diff;
          closest = i;
        }
      });
      slide_index = closest;
    }, 100);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.content-slide, .table-content');

  slides.forEach(slide => {
    const article = slide.querySelector('article, nav');
    if (!article) return;

    const textElements = article.querySelectorAll('p, li, ul, ol, blockquote');
    const originalSizes = Array.from(textElements).map(el =>
      parseFloat(getComputedStyle(el).fontSize)
    );

    let scaleStep = 1;
    const minFontSize = 12;

    const header = slide.querySelector('header');
    const headerHeight = header ? header.offsetHeight : 0;

    const computedSlideStyles = window.getComputedStyle(slide);
    const paddingTop = parseFloat(computedSlideStyles.paddingTop || 0);
    const paddingBottom = parseFloat(computedSlideStyles.paddingBottom || 0);

    const dynamicBuffer = headerHeight + paddingTop + paddingBottom;
    const maxArticleSize = slide.clientHeight - dynamicBuffer;

    const img = article.querySelector('img');
    if (img !== null) {
      img.style.setProperty('--max-article-size', `${maxArticleSize - 100}px`);
      void img.offsetWidth;
    }

    const setFontSize = (offset) => {
      textElements.forEach((el, idx) => {
        const newSize = Math.max(minFontSize, originalSizes[idx] - offset);
        el.style.fontSize = `${newSize}px`;
      });
    };

    const fitsInSlide = () => {
      slide.style.overflow = 'hidden';
      if (article.tagName.toLowerCase() !== 'nav') {
        return article.offsetHeight <= maxArticleSize;
      } else {
        return article.offsetHeight <= (maxArticleSize + (headerHeight / 2));
      }
    };

    while (!fitsInSlide() && originalSizes.some(s => s - scaleStep > minFontSize)) {
      setFontSize(scaleStep);
      scaleStep += 1;
    }

    if (!fitsInSlide()) {
      textElements.forEach((el, idx) => {
        el.style.fontSize = `${originalSizes[idx]}px`;
      });
      article.style.overflowY = 'auto';
      article.style.webkitOverflowScrolling = 'touch';
    }
  });
});

const scenarios = [
  {
    name: "Dynamic malware analysis",
    commands: [
      "C:\\Temp\\MalwareAnalysis> ",
      "python Win32Hooking sample.bin".split(''),
      "IAT call   KERNEL32.dll (target) LoadLibraryA: lpLibFileName = b'KernelBase.dll'",
      "\tIAT call   ntdll.dll (KERNELBASE.dll) NtQueryVirtualMemory: ProcessHandle = 18446744073709551615 (ffffffffffffffff) BaseAddress = 2748015230944 (27fd278bfe0) MemoryInformationClass = 0 (0) MemoryInformation = 568267302544 (844f5ee690) MemoryInformationLength = 48 (30) ReturnLength = 568267302440 (844f5ee628)",
      "\tIAT return ntdll.dll NtQueryVirtualMemory: 0 (0x0)",
      '\tIAT call   ntdll.dll (KERNELBASE.dll) LdrLoadDll: PathToFile = 1 (1) Flags = 568267302624 (844f5ee6e0) ModuleFileName = 568267302576 (844f5ee6b0) ModuleHandle = 568267302560 (844f5ee6a0)',
      '\t\tIAT call   ntdll.dll (KERNELBASE.dll) NtCreateFile: FileHandle = 568267296712 (844f5ecfc8) DesiredAccess = 1048704 (100080) ObjectAttributes = 568267296848 (844f5ed050) IoStatusBlock = 568267296760 (844f5ecff8) AllocationSize = None FileAttributes = 0 (0) ShareAccess = 7 (7) CreateDisposition = 1 (1) CreateOptions = 16416 (4020) EaBuffer = None EaLength = 0 (0)',
      '\t\tIAT return ntdll.dll NtCreateFile: 0 (0x0)',
      '\tIAT return ntdll.dll LdrLoadDll: 0 (0x0)',
      'IAT return KERNEL32.dll LoadLibraryA: 140733551411200 (0x7fff15570000)',
      "IAT call   KERNEL32.dll (target) GetProcAddress: hModule = 140733551411200 (7fff15570000) lpProcName = b'VirtualAlloc'",
      "\tGetProcAddress: Module = 0x7fff15570000 (KERNELBASE.dll), Function = VirtualAlloc, HookAddress = 0x27fd9380888",
      "IAT return KERNEL32.dll GetProcAddress: 2748128430216 (0x27fd9380888)",
      'GetProcAddress call   KERNELBASE.dll VirtualAlloc: lpAddress = None dwSize = 40 (28) flAllocationType = 12288 (3000) flProtect = 4 (4)',
      'GetProcAddress return KERNELBASE.dll VirtualAlloc: 2748128493568 (0x27fd9390000)',
      "IAT call   KERNEL32.dll (target) CreateThread: lpThreadAttributes = None dwStackSize = 0 (0) lpStartAddress = 2957203017728 (2b087091000) lpParameter = None dwCreationFlags = 0 (0) lpThreadId = None",
      "    IAT call   ntdll.dll (KERNELBASE.dll) NtCreateThreadEx: ThreadHandle = 1053233700144 (f5399edd30) DesiredAccess = 2097151 (1fffff) ObjectAttributes = None ProcessHandle = 18446744073709551615 (ffffffffffffffff) StartRoutine = 2957203017728 (2b087091000) Argument = None CreateFlags = 0 (0) ZeroBits = 0 (0) StackCommit = 0 (0) StackReserve = 0 (0) AttributeList = 1053233700416 (f5399ede40)",
      "        original call   ntdll.dll NtCreateThreadEx: ThreadHandle = 1053233700144 (f5399edd30) DesiredAccess = 2097151 (1fffff) ObjectAttributes = None ProcessHandle = 18446744073709551615 (ffffffffffffffff) StartRoutine = 2957203017728 (2b087091000) Argument = None CreateFlags = 0 (0) ZeroBits = 0 (0) StackCommit = 0 (0) StackReserve = 0 (0) AttributeList = 1053233700416 (f5399ede40)",
      "        modified call   ntdll.dll NtCreateThreadEx: ThreadHandle = 1053233700144 (f5399edd30) DesiredAccess = 2097151 (1fffff) ObjectAttributes = None ProcessHandle = 18446744073709551615 (ffffffffffffffff) StartRoutine = 2957335986176 (2b08ef60000) Argument = None CreateFlags = 0 (0) ZeroBits = 0 (0) StackCommit = 0 (0) StackReserve = 0 (0) AttributeList = 1053233700416 (f5399ede40)",
      "    IAT return ntdll.dll NtCreateThreadEx: 0x0",
      "IAT return KERNEL32.dll CreateThread: 700 (0x2bc)",
      "IAT call   KERNEL32.dll (target) WaitForSingleObject",
      "IAT return KERNEL32.dll WaitForSingleObject: None",
      "IAT call   KERNEL32.dll (target) CloseHandle",
      "IAT return KERNEL32.dll CloseHandle: 1 (0x1)",
      "IAT call   KERNEL32.dll (target) HeapAlloc: hHeap = 2907503198208 (2a4f4b20000) dwFlags = 8 (8) dwBytes = 968 (3c8)",
      "IAT return KERNEL32.dll HeapAlloc: 2907581933856 (0x2a4f9636920)",
    ]
  },
  {
    name: "Static heuristic malware analysis",
    commands: [
      "kali@kali:~$ ",
      "python3 -m ProgramExecutableAnalyzer sample.bin".split(''),
      "*************************************************************** DOS Headers ***************************************************************",
      "Magic                     00000000-00000002    4d5a                                     MZ                   Mark Zbikowski magic (MZ)",
      "************************************************************** Rich Headers ***************************************************************",
      "Checksum                  000000e4-000000e8    92cf9984                                 ....                 2224672658",
      "Calcul checksum           000000e4-000000e8    8499cf92                                 ....                 Valid checksum",
      "Rich header               00000080-000000e4    01048683                                 ....                 [ C ] VS2022 v17.12.2 build 34435",
      "Rich header               00000080-000000e4    01028683                                 ....                 [LNK] VS2022 v17.12.2 build 34435",
      "Rich header               00000080-000000e4    01038611                                 ....                 [ASM] VS2022 v17.12.0 pre 2.0 build 34321",
      "Rich header               00000080-000000e4    01048611                                 ....                 [ C ] VS2022 v17.12.0 pre 2.0 build 34321",
      "Rich header               00000080-000000e4    01058611                                 ....                 [C++] VS2022 v17.12.0 pre 2.0 build 34321",
      "Rich header               00000080-000000e4    00010000                                 ....                 [---] Unmarked objects",
      "*************************************************************** NT Headers ****************************************************************",
      "PE magic bytes            00000080-00000084    50450000                                 PE..                 Program Executable magic (PE)",
      "************************************************************ Optional Headers *************************************************************",
      "AddressEntryPoint         000000a8-000000ac    25110000                                 %...                 _start position: 4389",
      "SizeOfImage               000000d0-000000d4    00b00300                                 ....                 Image (memory) size: 241664",
      "DllCharacteristics        000000de-000000e0    6001                                     `.                   DLL can be relocated",
      "**************************************************************** Sections *****************************************************************",
      "Section .text             000001ac-000001b0    60005060                                 `.P`                 Read permissions",
      "Section .text             000001ac-000001b0    60005060                                 `.P`                 Executed as code",
      "Entry point section       000001ac-000001b0    60005060                                 `.P`                 .text",
      "*********************************************************** Functions imported ************************************************************",
      "Name                      000288c8-000288d4    4b45524e454c33322e646c6c                 KERNEL32.dll",
      "Function name             0002824e-0002825d    47657450726f6341646472657373             GetProcAddress",
      "Function name             0002833a-00028347    4c6f61644c69627261727941                 LoadLibraryA",
      "Function name             000282ce-000282db    4765745469636b436f756e74                 GetTickCount",
      "Function name             0002830e-00028320    4973446562756767657250726573656e74       IsDebuggerPresent",
      "Function name             00028360-0002836c    4f70656e50726f63657373                   OpenProcess",
      "Function name             000284f6-00028503    5669727475616c416c6c6f63                 VirtualAlloc",
      "Function name             00028514-00028523    5669727475616c50726f74656374             VirtualProtect",
    ]
  },
  {
    name: "Static malware analysis",
    commands: [
      "kali@kali:~$ ",
      "MagicStrings sample.bin".split(''),
      "[+] [0 string: string] thread",
      "[+] [0 string: string] libgcc_s_dw2-1.dll",
      "[+] [0 filename: string] libgcc_s_dw2-1.dll",
      "[+] [0 string: string] __register_frame_info",
      "[+] [0 string: string] __deregister_frame_info",
      "[+] [0 string: string] @EBIPExMUDxASFw8TFBsXFxcW",
      "[+] [5 linux_path: string, truncated, base64, crypto data, string, truncated] /334/027/34",
      "[+] [4 host_port: string, truncated, base64, crypto data, string] 13.225.136.25:6667",
      "[+] [4 ipv4: string, truncated, base64, crypto data, string] 13.225.136.25",
      "[+] [0 string: string] @SVVVUVIbDg5GERFGEEQPQk5MDkVOVk9NTkBFUg5SQEdEflRRRUBVRA9EWUQ=",
      "[+] [4 uri: string, truncated, base64, crypto data, string] https://g00g1e.com/downloads/safe_update.exe",
      "[+] [5 filename: string, truncated, base64, crypto data, string, truncated] g00g1e.com",
      "[+] [5 fqdn: string, truncated, base64, crypto data, string, truncated] g00g1e.com",
      "[+] [5 word: string, truncated, base64, crypto data, string, truncated] downloads",
      "[+] [5 filename: string, truncated, base64, crypto data, string, truncated] safe_update.exe",
      "[+] [5 fqdn: string, truncated, base64, crypto data, string, truncated] update.exe",
      "[+] [0 string: string] @ZkRVcVNOQmBFRVNEUlI=",
      "[+] [4 word: string, truncated, base64, crypto data, string] GetProcAddress",
      "[+] [0 string: string] @bU5ARW1IQ1NAU1hg",
      "[+] [4 word: string, truncated, base64, crypto data, string] LoadLibraryA",
      "[+] [0 string: string] GetModuleHandleA",
      "[+] [0 string: string] GetTickCount",
      "[+] [0 string: string] IsDebuggerPresent",
      "[+] [0 string: string] OpenProcess",
      "[+] [0 string: string] QueryPerformanceFrequency",
      "[+] [0 string: string] VirtualAlloc",
      "[+] [0 string: string] VirtualProtect",
      "[+] [0 string: string] WaitForSingleObject",
      "[+] [0 string: string] KERNEL32.dll",
      "[+] 52% |██████████          |",
    ]
  },
  {
    name: "Disk analysis using Python DiskAnalyzer.pyz",
    commands: [
      "kali@kali:~$ ",
      "python3 DiskAnalyzer.pyz".split(''),
      "[+] GPT Detected",
      "  GPT Signature       : EFI PART",
      "  GPT Disk GUID       : E3D9C96C-EF0D-46D2-9edd-d3de45386669",
      "  Partition Count     : 128",
      "  Partition Entry Size: 128",
      "  Partition Table LBA : 2",
      "",
      "[+] Partition Entries:",
      "  Partition 1:",
      "    Type GUID    : C12A7328-F81F-11D2-BA4B-00A0C93EC93B (PARTITION_SYSTEM_GUID)",
      "    Unique GUID  : 0FDD5358-F0E8-46B9-99c6-6aacacdf95bb",
      "    Start LBA    : 2048",
      "    End LBA      : 1023999",
      "    Size in MB   : 499.00 MB",
      "    Attributes   : 0x0 (0)",
      "    Partition Name: EFI system partition",
      "  Partition 2:",
      "    Type GUID    : E3C9E316-0B5C-4DB8-817D-F92DF00215AE (PARTITION_MSFT_RESERVED_GUID)",
      "    Unique GUID  : 643A339C-D349-4A2E-bab6-ce77fdb238e5",
      "    Start LBA    : 1024000",
      "    End LBA      : 1286143",
      "    Size in MB   : 128.00 MB",
      "    Attributes   : 0x0 (0)",
      "    Partition Name: Microsoft reserved partition",
      "  Partition 3:",
      "    Type GUID    : EBD0A0A2-B9E5-4433-87C0-68B6B72699C7 (PARTITION_BASIC_DATA_GUID)",
      "    Unique GUID  : 2DF35A88-AB62-4C1E-b8eb-aa1b57b83bbb",
      "    Start LBA    : 1286144",
      "    End LBA      : 990218239",
      "    Size in MB   : 482877.00 MB",
      "    Attributes   : 0x0 (0)",
      "    Partition Name: Basic data partition"
    ]
  },
  {
    name: "PDF forensic analysis with PDForensic",
    commands: [
      "kali@kali:~$ ",
      "PDForensic rTVEqzr.pdf".split(''),
      "-1        pdf_tag                   '%PDF-1.4\\n'",
      "-1        binary_tag                '%öäüß\\n'",
      "1         type                      Catalog",
      "6         date                      \"D:20250504133945+00'00'\"",
      "6         date                      \"D:20250504133945+00'00'\"",
      "2         type                      Pages",
      "7         type                      Page",
      "-1        xref",
      "-1        root                      '<<\\n/Root 1 0 R\\n/Info 6 0 R\\n/ID [<CCB6F70BF98CE32FA0B01B6BBEB6892A>'",
      "-1        unknow_token              '<CCB6F70BF98CE32FA0B01B6BBEB6892A>]'",
      "-1        unknow_token              '/Size'",
      "238       unknow_token              '238'",
      "-1        unknow_token              '>>'",
      "-1        startxref",
      "-1        eof_tag                   '%%EOF\\n'",
      "",
      "{",
      "    \"tool\": \"PDForensic\",",
      "    \"version\": \"0.2.1\",",
      "    \"file\": \"rTVEqzr.pdf\",",
      "    \"date\": \"2025-07-06T15:35:50.244925\",",
      "    \"malicious\": {",
      "        \"score\": \"0%\",",
      "        \"types\": []",
      "    },",
      "    \"objects\": {",
      "        \"found\": 247,",
      "        \"processed\": 237,",
      "        \"counter\": {",
      "            \"type - Catalog\": 1,",
      "            \"type - Pages\": 1,",
      "            \"type - Page\": 1,",
      "        }",
      "    }",
      "}"
    ]
  }
];

const timeoutIds = [];

function typeLines(lines, container, overlay, delay = 500) {
  let character_index = 0;
  let characters = null;
  let index = 0;
  container.innerText = '';

  const typeCharacter = () => {
    if (character_index < characters.length) {
      container.innerText += characters[character_index];
      character_index++;
      const id = setTimeout(typeCharacter, Math.random() * (delay / 10) + 50);
      timeoutIds.push(id);
    } else {
      container.innerText += '\n';
      const id = setTimeout(typeLine, Math.random() * delay + 50);
      timeoutIds.push(id);
      index++;
    }
  }

  const typeLine = () => {
    if (index < lines.length) {
      const value = lines[index];
      if (Array.isArray(value)) {
        characters = value;
        const id = setTimeout(typeCharacter, Math.random() * (delay / 10) + 50);
        timeoutIds.push(id);
      } else if (typeof value === 'string') {
        container.innerText += value;
        index++;
        if (index < lines.length && !Array.isArray(lines[index])) {
          container.innerText += '\n';
        }
        container.scrollTop = container.scrollHeight;
        const id = setTimeout(typeLine, Math.random() * delay + 50);
        timeoutIds.push(id);
      }
    } else {
      const id = setTimeout(triggerTerminalAnimation, 2000);
      timeoutIds.push(id);
    }
  };

  typeLine();
}

function triggerTerminalAnimation() {
  timeoutIds.forEach(clearTimeout);
  timeoutIds.length = 0;
  let activeScenario = scenarios[Math.floor(Math.random() * scenarios.length)];
  const overlay = document.getElementById('terminal-overlay');
  const output = document.getElementById('terminal-output');
  overlay.style.display = 'block';
  typeLines(activeScenario['commands'], output, overlay);
}

document.addEventListener('DOMContentLoaded', () => {
  let idleTimer;

  const overlay = document.getElementById('terminal-overlay');

  function resetIdleTimer() {
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      if (window.fullScreen && slide_index == 0) {
        overlay.style.display = 'block';
        triggerTerminalAnimation();
      }
    }, 20000);
  }

  function hideOverlay() {
    if (overlay.style.display === 'block') {
      overlay.style.display = 'none';
      timeoutIds.forEach(clearTimeout);
      timeoutIds.length = 0;
    }
    resetIdleTimer();
  }

  resetIdleTimer();

  ['mousemove', 'keydown', 'click', 'touchstart'].forEach(event => {
    document.addEventListener(event, hideOverlay);
  });
});
