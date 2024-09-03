/**
 * Converts HTML special characters like &<>"'`&rsquo; to & escaped codes or vice versa.
 * It handles named entities, decimal numeric character references, and hexadecimal numeric character references.
 *
 * @param {string} str - The string to process.
 * @param {boolean} unescape  default=true - If true, converts & codes to characters.
 *                                     If false, converts characters to codes.
 * @return {string} The processed string.
 * @category Extractor
 * @example
 * convertHTMLSpecialChars('&lt;p&gt;This &amp; that &copy; 2023 &quot;Quotes&quot; &#39;Apostrophes&#39; &euro;100 &#x263A;&lt;/p&gt;', true)
 * // Returns: "<p>This & that © 2023 "Quotes" 'Apostrophes' €100 ☺</p>"
 */
export function convertHTMLSpecialChars(str, unescape = true) {
  const entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    " ": "&nbsp;",
    "'": "&#39;",
    "`": "&#96;",
    "¢": "&cent;",
    "£": "&pound;",
    "¥": "&yen;",
    "€": "&euro;",
    "©": "&copy;",
    "®": "&reg;",
    "™": "&trade;",
  };

  // Add numeric character references for Latin-1 Supplement characters
  for (let i = 160; i <= 255; i++) {
    entityMap[String.fromCharCode(i)] = `&#${i};`;
  }

  if (unescape) {
    // Create a reverse mapping for unescaping
    const reverseEntityMap = Object.fromEntries(
      Object.entries(entityMap).map(([k, v]) => [v, k])
    );

    // Add alternative representations
    reverseEntityMap["&apos;"] = "'";
    reverseEntityMap["&laquo;"] = "«";
    reverseEntityMap["&raquo;"] = "»";

    // Regex to match all types of HTML entities
    const entityRegex = new RegExp(
      Object.keys(reverseEntityMap).join("|") + "|&#[0-9]+;|&#x[0-9a-fA-F]+;",
      "g"
    );

    str = str.replace(entityRegex, (entity) => {
      if (entity.startsWith("&#x")) {
        // Convert hexadecimal numeric character reference
        return String.fromCharCode(parseInt(entity.slice(3, -1), 16));
      } else if (entity.startsWith("&#")) {
        // Convert decimal numeric character reference
        return String.fromCharCode(parseInt(entity.slice(2, -1), 10));
      }
      // Convert named entity
      return reverseEntityMap[entity] || entity;
    });

    str = str.replace(/[\u0300-\u036f]/g, ""); //special chars

    return str;
  } else {
    // Regex to match all characters that need to be escaped
    const charRegex = new RegExp(`[${Object.keys(entityMap).join("")}]`, "g");
    return str.replace(charRegex, (char) => entityMap[char]);
  }
}
