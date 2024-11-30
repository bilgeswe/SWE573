// wikidata.js

const WikidataAPI = (() => {
    const apiUrl = 'https://www.wikidata.org/w/api.php';
    const sparqlEndpoint = 'https://query.wikidata.org/sparql';
    let defaultLimit = 10;

    function setDefaultLimit(limit) {
        defaultLimit = limit;
    }

    async function searchEntities(searchTerm, limit = defaultLimit, language = 'en') {
        if (!searchTerm) {
            return Promise.resolve([]);
        }

        const params = {
            action: 'wbsearchentities',
            format: 'json',
            language: language,
            uselang: language,
            search: searchTerm,
            limit: limit,
            origin: '*',
        };

        const url = `${apiUrl}?${new URLSearchParams(params).toString()}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            return data.search || [];
        } catch (error) {
            console.error('Wikidata API Error:', error);
            return [];
        }
    }

    async function getEntityDetails(entityId, languages = ['en']) {
        if (!entityId) {
            return Promise.reject(new Error('Entity ID is required.'));
        }

        const params = {
            action: 'wbgetentities',
            format: 'json',
            ids: entityId,
            languages: languages.join('|'),
            origin: '*',
        };

        const url = `${apiUrl}?${new URLSearchParams(params).toString()}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            return data.entities[entityId] || {};
        } catch (error) {
            console.error('Wikidata API Error:', error);
            return {};
        }
    }

    async function getRelatedEntities(entityId, relationshipType = 'P279') {
        if (!entityId) {
            return Promise.reject(new Error('Entity ID is required.'));
        }

        const query = `
            SELECT ?item ?itemLabel WHERE {
                wd:${entityId} wdt:${relationshipType} ?item .
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
        `;

        const url = `${sparqlEndpoint}?${new URLSearchParams({
            query: query,
            format: 'json',
        }).toString()}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            const results = data.results.bindings;
            return results.map(result_2 => ({
                id: result_2.item.value.split('/').pop(),
                label: result_2.itemLabel.value,
            }));
        } catch (error) {
            console.error('Wikidata SPARQL Error:', error);
            return [];
        }
    }

    async function listLanguages(entityId) {
        if (!entityId) {
            return Promise.reject(new Error('Entity ID is required.'));
        }

        const params = {
            action: 'wbgetentities',
            format: 'json',
            ids: entityId,
            props: 'labels',
            origin: '*',
        };

        const url = `${apiUrl}?${new URLSearchParams(params).toString()}`;

        return fetch(url)
            .then(response => response.json())
            .then(data => {
                const entity = data.entities[entityId];
                if (entity && entity.labels) {
                    return Object.keys(entity.labels);
                } else {
                    return [];
                }
            })
            .catch(error => {
                console.error('Wikidata API Error:', error);
                return [];
            });
    }

    return {
        searchEntities,
        getEntityDetails,
        getRelatedEntities,
        listLanguages,
        setDefaultLimit,
    };
})();

// Usage examples (uncomment to test):

// WikidataAPI.setDefaultLimit(5);
// WikidataAPI.searchEntities('Python').then(results => console.log(results));
// WikidataAPI.getEntityDetails('Q42').then(details => console.log(details));
// WikidataAPI.getRelatedEntities('Q42', 'P31').then(related => console.log(related));
// WikidataAPI.listLanguages('Q42').then(languages => console.log(languages));

