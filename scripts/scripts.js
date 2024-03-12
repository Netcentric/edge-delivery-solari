import {
  sampleRUM,
  // loadHeader,
  // loadFooter,
  addPageHeader,
  decorateButtons,
  decorateIcons,
  decorateSections,
  decorateBlocks,
  decorateTemplateAndTheme,
  decorateHeroH1,
  decorateGroups,
  waitForLCP,
  loadBlocks,
  loadCSS,
  getMetadata,
  decorateFocusPage,
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

function addShipSpecifications(specs, addIntroduction) {
  const infoContainer = document.createElement('div');
  const heroContainer = document.querySelector('.hero');

  if (specs.Range) {
    addSpeedInformation(specs.Range, infoContainer);
    addSpeedInformation(specs['Number of Passengers'].replace('to', '–').replaceAll(' ', ''), infoContainer, 'passengers', true);
    addSpeedInformation(specs.Length, infoContainer);
  }
  infoContainer.classList.add('info-container');
  heroContainer.append(infoContainer);

  const specContainer = document.createElement('div');
  specContainer.classList.add('spec-container');

  const introduction = addIntroduction ? `<h2>SPECIFICATIONS</h2><div><p>Learn more about the ${document.querySelector('h1').textContent} and its technical specifications.</p></div>` : '';
  const content = `${introduction}
  <div class="spec-table">
    <div class="spec-item">
      <div class="spec-title">Length</div>
      <div class="spec-value">${specs.Length.split(',')[0]}</div>
    </div>
    <div class="spec-item">
      <div class="spec-title">Width</div>
      <div class="spec-value">${specs.Width.split(',')[0]}</div>
    </div>
    <div class="spec-item">
      <div class="spec-title">Height</div>
      <div class="spec-value">${specs.Height.split(',')[0]}</div>
    </div>
    <div class="spec-item">
      <div class="spec-title">Weight</div>
      <div class="spec-value">${specs.Weight.split(',')[0]}</div>
    </div>
  </div>`;
  specContainer.innerHTML = content;

  const parentElement = document.querySelector('body .default-content-wrapper');
  parentElement.appendChild(specContainer);
}

function addEngineSpecifications(specs) {
  const specContainer = document.createElement('div');
  specContainer.classList.add('engine-spec-container');

  const content = `<table>
    <tr><td>Length</td><td>${specs.Length}</td></tr>
    <tr><td>Width</td><td>${specs.Width}</td></tr>
    <tr><td>Maximum Speed</td><td>${specs['Maximum Speed']}</td></tr>
    <tr><td>Range</td><td>${specs.Range}</td></tr>
  <table>`;
  specContainer.innerHTML = content;

  return specContainer;
}

async function prepareSpecification() {
  const isTemplate = (template) => document.body.classList.contains(template);
  const isShipFocus = isTemplate('ship-focus');
  const isEngineFocus = !isShipFocus && isTemplate('engine-focus');
  const isConfigurationResult = !isShipFocus && !isEngineFocus && isTemplate('configuration-result');
  try {
    const configurationsPromise = isConfigurationResult && fetch('/configurations.json');
    if (!isShipFocus && !isEngineFocus && !isConfigurationResult) {
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
    const findSpecification = (path) => specifications.data.find((s) => s.path === path);
    const specification = findSpecification(specificationUrl.pathname);
    if (!specification) {
      return;
    }

    const specificationsObj = JSON.parse(specification.specifications);

    if (isShipFocus || isConfigurationResult) {
      addShipSpecifications(specificationsObj, !isConfigurationResult);
    } else /* if (isEngineFocus) */ {
      const specContainer = addEngineSpecifications(specificationsObj);
      const parentElement = document.querySelector('body .default-content-wrapper .sub-group');

      parentElement.appendChild(specContainer);
    }

    if (isConfigurationResult) {
      const engineSpecificationUrl = getMetadata('engine-specifications');

      if (engineSpecificationUrl) {
        const engineSpecification = findSpecification(new URL(engineSpecificationUrl).pathname);

        document.body.dataset.engineSpecification = engineSpecification.specifications;

        if (engineSpecification) {
          const specContainer = addEngineSpecifications(
            JSON.parse(engineSpecification.specifications),
          );
          const engineDescription = document.querySelector('#engine ~ p + p');

          engineDescription.after(specContainer);
        }
      }
    }
    document.body.dataset.features = specification.features;
    document.body.dataset.specification = specification.specifications;

    if (configurationsPromise) {
      const configurationsResponse = await configurationsPromise;
      if (!configurationsResponse.ok) {
        return;
      }
      const configurations = await configurationsResponse.json();
      const configuration = configurations.data.find(
        (c) => c.configuration === window.location.pathname,
      );
      if (!configuration) {
        return;
      }
      document.querySelector('[id^="hello-traveler"]').textContent = `Hello ${configuration.firstName}`;
    }
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
  addPageHeader();
  decorateButtons(main);
  decorateIcons(main);
  decorateSections(main);
  decorateBlocks(main);
  decorateGroups();
  decorateHeroH1();
  decorateFocusPage('engine');
  decorateFocusPage('interior');
  decorateFocusPage('accessory');
  buildAutoBlocks(main);
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
