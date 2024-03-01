import {
  sampleRUM,
  // loadHeader,
  // loadFooter,
  decorateButtons,
  decorateIcons,
  decorateSections,
  decorateBlocks,
  decorateTemplateAndTheme,
  decorateSpaceshipFocusPageH1,
  decorateGroups,
  waitForLCP,
  loadBlocks,
  loadCSS,
  getMetadata,
} from './aem.js';

const LCP_BLOCKS = []; // add your LCP blocks to the list

function addSpeedInformation(info, containerElement, name, splitWords = false) {
  const infoElement = document.createElement('div');

  infoElement.classList.add('info');

  const texts = info.split(' ');
  const result = `<span class="info-number">${splitWords ? info : texts[0]}</span><span class="info-text">${splitWords ? name : texts.slice(1).join(' ')}</span>`;

  infoElement.innerHTML = result;
  containerElement.appendChild(infoElement);
}

function addSpecifications(specs) {
  const specContainer = document.createElement('div');

  specContainer.classList.add('spec-container');

  const content = `<h2>SPECIFICATIONS</h2><div><p>Learn more about the ${document.querySelector('h1').textContent} and its technical specifications.</p></div>
  <table class="spec-table"><tr><th>length</th><th>width</th><th>height</th><th>weight</th></tr>
  <tr><td>${specs.Length.split(',')[0]}</td><td>${specs.Width.split(',')[0]}</td><td>${specs.Height.split(',')[0]}</td><td>${specs.Weight.split(',')[0]}</td></tr><table></div>`;
  specContainer.innerHTML = content;

  const parentElement = document.querySelector('body.ship-focus .default-content-wrapper');
  parentElement.appendChild(specContainer);
}

async function prepareSpecification() {
  try {
    if (!document.body.classList.contains('ship-focus')) {
      return;
    }
    const specificationPath = getMetadata('specifications');
    if (!specificationPath) {
      return;
    }
    const specificationUrl = new URL(specificationPath);
    const specificationsResponse = await fetch('/specifications/query-index.json');
    if (!specificationsResponse.ok) {
      return;
    }
    const specifications = await specificationsResponse.json();
    const specification = specifications.data.find((s) => s.path === specificationUrl.pathname);
    if (!specification) {
      return;
    }

    const specificationsObj = JSON.parse(specification.specifications);
    const infoContainer = document.createElement('div');
    const titleElement = document.querySelector('h2');

    if (specificationsObj.Range) {
      addSpeedInformation(specificationsObj.Range, infoContainer);
      // Temp content as it is not received from document
      addSpeedInformation(specificationsObj['Number of Passengers'].replace('to', '–').replaceAll(' ', ''), infoContainer, 'passengers', true);
      addSpeedInformation(specificationsObj.Length, infoContainer);
    }

    addSpecifications(specificationsObj);

    infoContainer.classList.add('info-container');
    titleElement.parentNode.insertBefore(infoContainer, titleElement);

    // these dataset are reference and will be removed later
    document.body.dataset.features = specification.features;
    document.body.dataset.specification = specification.specifications;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.error('could not load specifications', e);
  }
}

/**
 * load fonts.css and set a session storage flag
 */
async function loadFonts() {
  await loadCSS(`${window.hlx.codeBasePath}/styles/fonts.css`);
  try {
    if (!window.location.hostname.includes('localhost')) sessionStorage.setItem('fonts-loaded', 'true');
  } catch (e) {
    // do nothing
  }
}

/**
 * Builds all synthetic blocks in a container element.
 * @param {Element} main The container element
 */
function buildAutoBlocks(main) {
  try {
    prepareSpecification(main);
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Auto Blocking failed', error);
  }
}

/**
 * Decorates the main element.
 * @param {Element} main The main element
 */
// eslint-disable-next-line import/prefer-default-export
export function decorateMain(main) {
  // hopefully forward compatible button decoration
  decorateButtons(main);
  decorateIcons(main);
  buildAutoBlocks(main);
  decorateSections(main);
  decorateBlocks(main);
  decorateGroups();
  decorateSpaceshipFocusPageH1();
}

/**
 * Loads everything needed to get to LCP.
 * @param {Element} doc The container element
 */
async function loadEager(doc) {
  document.documentElement.lang = 'en';
  decorateTemplateAndTheme();
  const main = doc.querySelector('main');
  if (main) {
    decorateMain(main);
    document.body.classList.add('appear');
    await waitForLCP(LCP_BLOCKS);
  }

  try {
    /* if desktop (proxy for fast connection) or fonts already loaded, load fonts.css */
    if (window.innerWidth >= 900 || sessionStorage.getItem('fonts-loaded')) {
      loadFonts();
    }
  } catch (e) {
    // do nothing
  }
}

/**
 * Loads everything that doesn't need to be delayed.
 * @param {Element} doc The container element
 */
async function loadLazy(doc) {
  const main = doc.querySelector('main');
  await loadBlocks(main);

  const { hash } = window.location;
  const element = hash ? doc.getElementById(hash.substring(1)) : false;
  if (hash && element) element.scrollIntoView();

  // loadHeader(doc.querySelector('header'));
  // loadFooter(doc.querySelector('footer'));

  loadCSS(`${window.hlx.codeBasePath}/styles/lazy-styles.css`);
  loadFonts();

  sampleRUM('lazy');
  sampleRUM.observe(main.querySelectorAll('div[data-block-name]'));
  sampleRUM.observe(main.querySelectorAll('picture > img'));
}

/**
 * Loads everything that happens a lot later,
 * without impacting the user experience.
 */
function loadDelayed() {
  // eslint-disable-next-line import/no-cycle
  window.setTimeout(() => import('./delayed.js'), 3000);
  // load anything that can be postponed to the latest here
}

async function loadPage() {
  await loadEager(document);
  await loadLazy(document);
  loadDelayed();
}

loadPage();
