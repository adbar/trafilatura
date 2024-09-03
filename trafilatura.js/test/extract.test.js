import { test, expect, it } from "vitest";
var { extract } = require("../core.js");
var { extractContentHTML } = require("../readability_lxml.js");

test("readability - should extract content from HTML", async () => {
  var url = "https://en.wikipedia.org/wiki/David_Hilbert";
  var html = await (await fetch(url)).text();

  // var content = extract(html, {url});
  var content = extractContentHTML(html);
  console.log(content.innerHTML);



  expect(content).toBeDefined();
});


test("trafilatura - should extract content from HTML", async () => {
 
  var url = "https://en.wikipedia.org/wiki/David_Hilbert";
  var html = await (await fetch(url)).text();

  var content = extract(html, { url });
  console.log(content);

  expect(content.length).toBeGreaterThan(100);
});
