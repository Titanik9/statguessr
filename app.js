(function () {
  const TOTAL_ROUNDS = 5;
  const WORLD_VIEW = {
    center: [20, 5],
    zoom: 2.2,
  };

  const METRIC_CONFIG = {
    rent: {
      label: "1BR downtown rent",
      note: "Monthly, USD",
      format: (value) =>
        `$${Math.round(value).toLocaleString("en-US")}/mo`,
    },
    cappuccino: {
      label: "Cappuccino",
      note: "Regular size",
      format: (value) => `$${value.toFixed(2)}`,
    },
    gym: {
      label: "Gym membership",
      note: "Monthly, USD",
      format: (value) => `$${Math.round(value).toLocaleString("en-US")}/mo`,
    },
    crime: {
      label: "Crime rate",
      note: "Numbeo crime index",
      format: (value) => value.toFixed(1),
    },
    commute: {
      label: "Commute time",
      note: "Average trip length",
      format: (value) => `${Math.round(value)} min`,
    },
    pollution: {
      label: "Pollution",
      note: "Numbeo pollution index",
      format: (value) => value.toFixed(1),
    },
    salary: {
      label: "Net salary",
      note: "Monthly, USD",
      format: (value) =>
        `$${Math.round(value).toLocaleString("en-US")}/mo`,
    },
    transitPass: {
      label: "Transit pass",
      note: "Monthly, USD",
      format: (value) => `$${Math.round(value).toLocaleString("en-US")}/mo`,
    },
  };

  const coreClues = ["rent", "cappuccino", "gym", "crime", "commute", "pollution"];
  const bonusClues = ["salary", "transitPass"];
  const cities = Array.isArray(window.STATGUESSR_CITIES)
    ? window.STATGUESSR_CITIES
    : [];

  const elements = {
    clueCards: document.getElementById("clueCards"),
    clueHeading: document.getElementById("clueHeading"),
    statusBadge: document.getElementById("statusBadge"),
    roundValue: document.getElementById("roundValue"),
    scoreValue: document.getElementById("scoreValue"),
    seedValue: document.getElementById("seedValue"),
    submitGuessButton: document.getElementById("submitGuessButton"),
    nextRoundButton: document.getElementById("nextRoundButton"),
    summaryCard: document.getElementById("summaryCard"),
    roundScoreValue: document.getElementById("roundScoreValue"),
    summaryText: document.getElementById("summaryText"),
    distanceText: document.getElementById("distanceText"),
    historyBar: document.getElementById("historyBar"),
    historyCaption: document.getElementById("historyCaption"),
    newChallengeButton: document.getElementById("newChallengeButton"),
    shareSeedButton: document.getElementById("shareSeedButton"),
  };

  const state = {
    seed: "",
    rounds: [],
    currentRoundIndex: 0,
    totalScore: 0,
    currentGuess: null,
    roundResults: [],
    mapReady: false,
  };

  let map;
  let guessMarker;
  let answerMarker;
  let guideLine;

  init();

  function init() {
    initMap();
    bindEvents();

    if (cities.length < TOTAL_ROUNDS) {
      showDataError();
      return;
    }

    const seedFromUrl = new URLSearchParams(window.location.search).get("seed");
    startGame(seedFromUrl || createSeed());
  }

  function initMap() {
    map = L.map("map", {
      worldCopyJump: false,
      minZoom: 2,
      maxZoom: 6,
      zoomSnap: 0.25,
      maxBounds: [
        [-80, -180],
        [85, 180],
      ],
      maxBoundsViscosity: 0.85,
    }).setView(WORLD_VIEW.center, WORLD_VIEW.zoom);

    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png",
      {
        subdomains: "abcd",
        noWrap: true,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
      }
    ).addTo(map);

    map.on("click", handleMapClick);
    state.mapReady = true;
  }

  function bindEvents() {
    elements.submitGuessButton.addEventListener("click", submitGuess);
    elements.nextRoundButton.addEventListener("click", goToNextRound);
    elements.newChallengeButton.addEventListener("click", () => startGame(createSeed()));
    elements.shareSeedButton.addEventListener("click", copySeedLink);
  }

  function showDataError() {
    elements.clueHeading.textContent = "Dataset missing";
    elements.statusBadge.textContent = "Run the data fetch script first";
    elements.clueCards.innerHTML =
      '<article class="clue-card" style="opacity:1;transform:none;animation:none;"><span class="clue-name">No city data found</span><span class="clue-note">Generate the Numbeo snapshot with `python3 tools/fetch_numbeo.py`, then reload this page.</span></article>';
    elements.submitGuessButton.disabled = true;
    elements.newChallengeButton.disabled = true;
    elements.shareSeedButton.disabled = true;
    renderHistory();
  }

  function startGame(seed) {
    const normalizedSeed = normalizeSeed(seed);
    const rng = mulberry32(hashSeed(normalizedSeed));
    const shuffledCities = shuffle(cities.slice(), rng);
    const roundCities = shuffledCities.slice(0, TOTAL_ROUNDS);

    state.seed = normalizedSeed;
    state.rounds = roundCities.map((city) => ({
      city,
      clues: selectClues(city.metrics, rng),
      guessed: false,
    }));
    state.currentRoundIndex = 0;
    state.totalScore = 0;
    state.currentGuess = null;
    state.roundResults = [];

    updateSeedInUrl(normalizedSeed);
    clearMapArtifacts();
    resetMapView();
    renderRound();
    renderHistory();
  }

  function renderRound() {
    const round = getCurrentRound();
    if (!round) {
      renderGameOver();
      return;
    }

    state.currentGuess = null;
    clearMapArtifacts();
    resetMapView();

    elements.roundValue.textContent = `${state.currentRoundIndex + 1} / ${TOTAL_ROUNDS}`;
    elements.scoreValue.textContent = formatScore(state.totalScore);
    elements.seedValue.textContent = state.seed;
    elements.clueHeading.textContent = "Find the hidden city";
    elements.statusBadge.textContent = "Pick a spot on the map";
    elements.summaryCard.hidden = true;
    elements.submitGuessButton.hidden = false;
    elements.submitGuessButton.disabled = true;
    elements.nextRoundButton.hidden = true;
    elements.historyCaption.textContent = "Five rounds per challenge";

    elements.clueCards.innerHTML = "";
    round.clues.forEach((metricKey, index) => {
      const metric = METRIC_CONFIG[metricKey];
      const value = round.city.metrics[metricKey];
      const card = document.createElement("article");
      card.className = "clue-card";
      card.style.animationDelay = `${index * 60}ms`;
      card.innerHTML = `
        <span class="clue-name">${metric.label}</span>
        <span class="clue-value">${metric.format(value)}</span>
        <span class="clue-note">${metric.note}</span>
      `;
      elements.clueCards.appendChild(card);
    });

    renderHistory();
  }

  function renderGameOver() {
    const bestPossible = TOTAL_ROUNDS * 5000;
    const performance = Math.round((state.totalScore / bestPossible) * 100);

    elements.roundValue.textContent = `${TOTAL_ROUNDS} / ${TOTAL_ROUNDS}`;
    elements.scoreValue.textContent = formatScore(state.totalScore);
    elements.seedValue.textContent = state.seed;
    elements.clueHeading.textContent = "Challenge complete";
    elements.statusBadge.textContent = `${performance}% of the perfect score`;
    elements.submitGuessButton.hidden = true;
    elements.nextRoundButton.hidden = true;
    elements.summaryCard.hidden = false;
    elements.roundScoreValue.textContent = formatScore(state.totalScore);
    elements.summaryText.textContent = `You finished the seed "${state.seed}" with ${formatScore(
      state.totalScore
    )} points across ${TOTAL_ROUNDS} rounds.`;
    elements.distanceText.textContent =
      "Start a new challenge for a fresh mix of cities, or share this seed so other players can tackle the same board.";
    elements.historyCaption.textContent = "Share the seed to run the same challenge";

    resetMapView();
    renderHistory(true);
  }

  function handleMapClick(event) {
    if (!getCurrentRound() || getCurrentRound().guessed) {
      return;
    }

    state.currentGuess = {
      lat: event.latlng.lat,
      lng: event.latlng.lng,
    };

    if (!guessMarker) {
      guessMarker = createCircleMarker(state.currentGuess, {
        color: "#ffb25b",
        fillColor: "#ff7f41",
      }).addTo(map);
    } else {
      guessMarker.setLatLng(state.currentGuess);
    }

    elements.statusBadge.textContent = "Guess pinned. Lock it in when ready.";
    elements.submitGuessButton.disabled = false;
  }

  function submitGuess() {
    const round = getCurrentRound();
    if (!round || round.guessed || !state.currentGuess) {
      return;
    }

    const actual = {
      lat: round.city.lat,
      lng: round.city.lng,
    };
    const distance = haversineKm(state.currentGuess, actual);
    const score = distanceToScore(distance);
    const accuracy = describeAccuracy(distance);

    round.guessed = true;
    state.totalScore += score;
    state.roundResults.push({
      round: state.currentRoundIndex + 1,
      city: round.city.label,
      score,
      distance,
    });

    if (!answerMarker) {
      answerMarker = createCircleMarker(actual, {
        color: "#78d5c7",
        fillColor: "#0ea5a3",
      }).addTo(map);
    } else {
      answerMarker.setLatLng(actual).addTo(map);
    }

    if (!guideLine) {
      guideLine = L.polyline([state.currentGuess, actual], {
        color: "#f4efe5",
        weight: 2,
        dashArray: "8 10",
        opacity: 0.8,
      }).addTo(map);
    } else {
      guideLine.setLatLngs([state.currentGuess, actual]).addTo(map);
    }

    map.fitBounds(L.latLngBounds([state.currentGuess, actual]), {
      padding: [56, 56],
      maxZoom: 4,
    });

    elements.scoreValue.textContent = formatScore(state.totalScore);
    elements.statusBadge.textContent = accuracy;
    elements.summaryCard.hidden = false;
    elements.roundScoreValue.textContent = formatScore(score);
    elements.summaryText.textContent = `The answer was ${round.city.label}. ${accuracy}`;
    elements.distanceText.textContent = `${formatDistance(distance)} away from your guess.`;
    elements.submitGuessButton.hidden = true;
    elements.nextRoundButton.hidden = false;
    renderHistory();
  }

  function goToNextRound() {
    if (!getCurrentRound() || !getCurrentRound().guessed) {
      return;
    }

    state.currentRoundIndex += 1;
    renderRound();
  }

  function renderHistory(showFinalState) {
    elements.historyBar.innerHTML = "";

    for (let index = 0; index < TOTAL_ROUNDS; index += 1) {
      const pill = document.createElement("article");
      const result = state.roundResults[index];
      pill.className = "history-pill";

      if (!result) {
        pill.classList.add("is-pending");
        pill.innerHTML = `<span>Round ${index + 1}</span><strong>${
          showFinalState ? "missed" : "pending"
        }</strong>`;
      } else {
        pill.innerHTML = `<span>Round ${index + 1}</span><strong>${formatScore(
          result.score
        )}</strong>`;
      }

      elements.historyBar.appendChild(pill);
    }
  }

  function clearMapArtifacts() {
    [guessMarker, answerMarker, guideLine].forEach((layer) => {
      if (layer && map.hasLayer(layer)) {
        map.removeLayer(layer);
      }
    });
    guessMarker = null;
    answerMarker = null;
    guideLine = null;
  }

  function resetMapView() {
    if (!state.mapReady) {
      return;
    }

    map.setView(WORLD_VIEW.center, WORLD_VIEW.zoom);
  }

  function createCircleMarker(latlng, options) {
    return L.circleMarker(latlng, {
      radius: 8,
      weight: 3,
      color: options.color,
      fillColor: options.fillColor,
      fillOpacity: 0.9,
    });
  }

  function selectClues(metrics, rng) {
    const totalCount = randomInt(rng, 5, 8);
    const selected = shuffle(coreClues.slice(), rng).slice(
      0,
      Math.min(totalCount, coreClues.length)
    );

    if (selected.length < totalCount) {
      const extrasNeeded = totalCount - selected.length;
      selected.push(...shuffle(bonusClues.slice(), rng).slice(0, extrasNeeded));
    }

    return Object.keys(METRIC_CONFIG).filter((key) => selected.includes(key));
  }

  function getCurrentRound() {
    return state.rounds[state.currentRoundIndex];
  }

  function distanceToScore(distance) {
    return Math.max(0, Math.round(5000 * Math.exp(-distance / 2100)));
  }

  function describeAccuracy(distance) {
    if (distance < 100) return "Bullseye territory.";
    if (distance < 400) return "Very sharp guess.";
    if (distance < 900) return "Strong regional read.";
    if (distance < 1800) return "You were in the right neighborhood.";
    if (distance < 3500) return "Same broad part of the world.";
    return "The stats sent you somewhere else entirely.";
  }

  function formatScore(score) {
    return score.toLocaleString("en-US");
  }

  function formatDistance(distance) {
    return `${Math.round(distance).toLocaleString("en-US")} km`;
  }

  function haversineKm(pointA, pointB) {
    const toRad = (deg) => (deg * Math.PI) / 180;
    const earthRadiusKm = 6371;
    const dLat = toRad(pointB.lat - pointA.lat);
    const dLng = toRad(pointB.lng - pointA.lng);
    const lat1 = toRad(pointA.lat);
    const lat2 = toRad(pointB.lat);

    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.sin(dLng / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);

    return 2 * earthRadiusKm * Math.asin(Math.sqrt(a));
  }

  function createSeed() {
    return Math.random().toString(36).slice(2, 8).toUpperCase();
  }

  function normalizeSeed(seed) {
    return (seed || createSeed())
      .toString()
      .trim()
      .toUpperCase()
      .replace(/[^A-Z0-9]/g, "")
      .slice(0, 12) || createSeed();
  }

  function hashSeed(input) {
    let hash = 1779033703 ^ input.length;
    for (let index = 0; index < input.length; index += 1) {
      hash = Math.imul(hash ^ input.charCodeAt(index), 3432918353);
      hash = (hash << 13) | (hash >>> 19);
    }

    return function () {
      hash = Math.imul(hash ^ (hash >>> 16), 2246822507);
      hash = Math.imul(hash ^ (hash >>> 13), 3266489909);
      return (hash ^= hash >>> 16) >>> 0;
    };
  }

  function mulberry32(seedFactory) {
    let seed = seedFactory();
    return function () {
      seed += 0x6d2b79f5;
      let result = Math.imul(seed ^ (seed >>> 15), seed | 1);
      result ^= result + Math.imul(result ^ (result >>> 7), result | 61);
      return ((result ^ (result >>> 14)) >>> 0) / 4294967296;
    };
  }

  function shuffle(items, rng) {
    for (let index = items.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(rng() * (index + 1));
      [items[index], items[swapIndex]] = [items[swapIndex], items[index]];
    }
    return items;
  }

  function randomInt(rng, min, max) {
    return Math.floor(rng() * (max - min + 1)) + min;
  }

  function updateSeedInUrl(seed) {
    const url = new URL(window.location.href);
    url.searchParams.set("seed", seed);
    window.history.replaceState({}, "", url);
  }

  async function copySeedLink() {
    const url = new URL(window.location.href);
    url.searchParams.set("seed", state.seed);

    try {
      await navigator.clipboard.writeText(url.toString());
      elements.statusBadge.textContent = "Seed link copied to clipboard";
    } catch (error) {
      elements.statusBadge.textContent = "Copy failed. The link is still in the address bar.";
    }
  }
})();
