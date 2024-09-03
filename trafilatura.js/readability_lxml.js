import { JSDOM } from 'jsdom';

/**
 * Extracts main content from HTML documents using Readability algorithm.
 * Employs regex patterns, HTML cleaning, node scoring, and content selection.
 * 
 * 1. Define regex patterns for content identification
 * 2. Clean HTML by removing unlikely content
 * 3. Score nodes based on content quality indicators
 * 4. Select the best candidate for main content
 * 5. Extract and clean the selected content
 * 
 * @param {string} html The HTML string to parse.
 * @param {Object} options Configuration options for parsing.
 * @returns {string} Parsed content and readability assessment.
 * 
 * @license Apache-2.0
 * Based on Mozilla (2015), Arc90 (2010) [github](https://github.com/mozilla/readability)
 * @see {@link https://github.com/scrapinghub/article-extraction-benchmark?tab=readme-ov-file#results|Article extraction benchmark}
 */
export function extractContentHTML(html, options = {}) {
    // Initialize configuration options
    const minContentLength = options.minContentLength || 140;
    const minScore = options.minScore || 20;
    const minTextLength = options.minTextLength || 25;
    const retryLength = options.retryLength || 250;

    // Step 1: Define regex patterns and constants
    const DOT_SPACE = /\.( |$)/;
    const DIV_TO_P_ELEMS = new Set(["a", "blockquote", "dl", "div", "img", "ol", "p", "pre", "table", "ul"]);
    const DIV_SCORES = new Set(["div", "article"]);
    const BLOCK_SCORES = new Set(["pre", "td", "blockquote"]);
    const BAD_ELEM_SCORES = new Set(["address", "ol", "ul", "dl", "dd", "dt", "li", "form", "aside"]);
    const STRUCTURE_SCORES = new Set(["h1", "h2", "h3", "h4", "h5", "h6", "th", "header", "footer", "nav"]);
    const TEXT_CLEAN_ELEMS = new Set(["p", "img", "li", "a", "embed", "input"]);
    const FRAME_TAGS = new Set(["body", "html"]);
    const LIST_TAGS = new Set(["ol", "ul"]);

    const REGEXES = {
        unlikelyCandidatesRe: /combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|pagination|pager|popup|tweet|twitter/i,
        okMaybeItsACandidateRe: /and|article|body|column|main|shadow/i,
        positiveRe: /article|body|content|entry|hentry|main|page|pagination|post|text|blog|story/i,
        negativeRe: /button|combx|comment|com-|contact|figure|foot|footer|footnote|form|input|masthead|media|meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget/i,
        divToPElementsRe: /<(?:a|blockquote|dl|div|img|ol|p|pre|table|ul)/i,
        videoRe: /https?:\/\/(?:www\.)?(?:youtube|vimeo)\.com/i,
    };

    class Candidate {
        constructor(score, elem) {
            this.score = score;
            this.elem = elem;
        }
    }


    // Helper: Get inner text with optional space normalization
    function getInnerText(elem, normalizeSpaces = true) {
        if (!elem) return '';
        let textContent = elem.textContent || '';
        textContent = textContent.trim();
        return normalizeSpaces ? textContent.replace(/\s+/g, ' ') : textContent;
    }

    // Helper: Calculate link density
    function getLinkDensity(elem) {
        if (!elem) return 0;
        const textLength = getInnerText(elem).length;
        if (textLength === 0) return 0;
        const linkLength = Array.from(elem.querySelectorAll('a'))
            .reduce((acc, link) => acc + getInnerText(link).length, 0);
        return linkLength / textLength;
    }

    // Step 4: Define scoring function
    function classWeight(elem) {
        let weight = 0;
        if (elem.getAttribute('class')) {
            if (REGEXES.negativeRe.test(elem.getAttribute('class'))) weight -= 25;
            if (REGEXES.positiveRe.test(elem.getAttribute('class'))) weight += 25;
        }
        if (elem.getAttribute('id')) {
            if (REGEXES.negativeRe.test(elem.getAttribute('id'))) weight -= 25;
            if (REGEXES.positiveRe.test(elem.getAttribute('id'))) weight += 25;
        }
        return weight;
    }

    function scoreNode(elem) {
        var score = classWeight(elem);
        var name = elem.tagName.toLowerCase();
        if (DIV_SCORES.has(name)) score += 5;
        else if (BLOCK_SCORES.has(name)) score += 3;
        else if (BAD_ELEM_SCORES.has(name)) score -= 3;
        else if (STRUCTURE_SCORES.has(name)) score -= 5;
        return new Candidate(score, elem);
    }

    // Step 3: Clean HTML
    function removeUnlikelyCandidates(doc) {
        for (var elem of doc.querySelectorAll('*')) {
            var attrs = (elem.getAttribute('class') || '') + ' ' + (elem.getAttribute('id') || '');
            if (attrs.length < 2) continue;
            if (!FRAME_TAGS.has(elem.tagName.toLowerCase()) &&
                REGEXES.unlikelyCandidatesRe.test(attrs) &&
                !REGEXES.okMaybeItsACandidateRe.test(attrs)) {
                elem.remove();
            }
        }
    }

    function transformMisusedDivsIntoParagraphs(doc) {
        var divs = doc.getElementsByTagName('div');
        for (var elem of divs) {
            if (!REGEXES.divToPElementsRe.test(elem.innerHTML.replace(/\s+/, ' '))) {
                // Convert div to paragraph if it doesn't contain block elements
                // elem.tagName = 'p';
            }
        }
    }

    // Step 4: Score paragraphs
    function scoreParagraphs(doc) {
        var candidates = {};
        var elems = doc.querySelectorAll('p, pre, td');
    
        for (var elem of elems) {
            var parentNode = elem.parentNode;
            var grandParentNode = parentNode ? parentNode.parentNode : null;
    
            var innerText = getInnerText(elem);
            var innerTextLen = innerText.length;

            if (innerTextLen < minTextLength) continue;

            if (!candidates[parentNode]) candidates[parentNode] = scoreNode(parentNode);
            if (grandParentNode && !candidates[grandParentNode]) candidates[grandParentNode] = scoreNode(grandParentNode);

            var score = 1 + innerText.split(',').length + Math.min((innerTextLen / 100), 3);

            candidates[parentNode].score += score;
            if (grandParentNode) candidates[grandParentNode].score += score / 2;
        }

        // Adjust scores based on link density
        for (var [elem, candidate] of Object.entries(candidates)) {
            candidate.score *= (1 - getLinkDensity(elem));
        }

        return candidates;
    }

    // Step 5: Select best candidate
    function selectBestCandidate(candidates) {
        var sortedCandidates = Object.values(candidates).sort((a, b) => b.score - a.score);
        return sortedCandidates[0];
    }

    // Step 6: Extract content
    function getArticle(doc, candidates, bestCandidate) {
        var siblingScoreThreshold = Math.max(10, bestCandidate.score * 0.2);
        var output = doc.createElement('div');
        var parent = bestCandidate.elem.parentNode;
        var siblings = parent ? Array.from(parent.children) : [bestCandidate.elem];

        for (var sibling of siblings) {
            let append = false;
            if (sibling === bestCandidate.elem || (candidates[sibling] && candidates[sibling].score >= siblingScoreThreshold)) {
                append = true;
            } else if (sibling.tagName === 'P') {
                var linkDensity = getLinkDensity(sibling);
                var nodeContent = sibling.textContent;
                var nodeLength = nodeContent.length;

                if (nodeLength > 80 && linkDensity < 0.25 || (nodeLength <= 80 && linkDensity === 0 && DOT_SPACE.test(nodeContent))) {
                    append = true;
                }
            }

            if (append) output.appendChild(sibling.cloneNode(true));
        }

        return output;
    }

    // Step 6 (continued): Clean extracted content
    function sanitize(node, candidates) {
        // Remove unwanted elements
        for (var elem of node.querySelectorAll('h1, h2, h3, h4, h5, h6, form, textarea, iframe')) {
            if (elem.tagName === 'IFRAME' && REGEXES.videoRe.test(elem.src)) {
                elem.textContent = 'VIDEO';
            } else {
                elem.remove();
            }
        }

        // Clean remaining elements
        var allowed = new Set();
        for (var elem of Array.from(node.querySelectorAll('table, ul, div, aside, header, footer, section')).reverse()) {
            if (allowed.has(elem)) continue;
            
            var weight = classWeight(elem);
            var score = candidates[elem] ? candidates[elem].score : 0;
            
            if (weight + score < 0) {
                elem.remove();
            } else if (elem.textContent.split(',').length < 10) {
                var counts = {
                    p: elem.querySelectorAll('p').length,
                    img: elem.querySelectorAll('img').length,
                    li: Math.max(0, elem.querySelectorAll('li').length - 100),
                    input: elem.querySelectorAll('input').length - elem.querySelectorAll('input[type=hidden]').length,
                    a: elem.querySelectorAll('a').length
                };
                var contentLength = getInnerText(elem).length;
                var linkDensity = getLinkDensity(elem);
                
                // Remove element if it meets certain criteria
                if ((counts.img > 1 + counts.p * 1.3) ||
                    (counts.li > counts.p && elem.tagName !== 'UL' && elem.tagName !== 'OL') ||
                    (counts.input > counts.p / 3) ||
                    (contentLength < minTextLength && counts.img === 0) ||
                    (weight < 25 && linkDensity > 0.2) ||
                    (weight >= 25 && linkDensity > 0.5) ||
                    ((counts.embed === 1 && contentLength < 75) || counts.embed > 1)) {
                    elem.remove();
                }
            }
        }

        return node;
    }

   
    // Main logic
    const dom = new JSDOM(html);
    const doc = dom.window.document;

    // Remove script and style tags
    doc.querySelectorAll('script, style').forEach(elem => elem.remove());

    let ruthless = true;
    while (true) {
        if (ruthless) {
            removeUnlikelyCandidates(doc);  // Step 3: Clean HTML
        }
        transformMisusedDivsIntoParagraphs(doc);  // Step 3: Clean HTML
        var candidates = scoreParagraphs(doc);  // Step 4: Score nodes

        var bestCandidate = selectBestCandidate(candidates);  // Step 5: Select best candidate

        if (bestCandidate) {
            var article = getArticle(doc, candidates, bestCandidate);  // Step 6: Extract content
            var cleanedArticle = sanitize(article, candidates);  // Step 6: Clean extracted content
            var articleLength = cleanedArticle ? cleanedArticle.textContent.length : 0;
            if (ruthless && articleLength < retryLength) {
                ruthless = false;
                continue;
            }
            return  cleanedArticle
        } else {
            if (ruthless) {
                ruthless = false;
                continue;
            }
            var article = doc.querySelector('body') || doc;
            return sanitize(article, candidates)
        }
    }
}
