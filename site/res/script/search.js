document.addEventListener("DOMContentLoaded", () => {
    // we're clearly running javascript, so get rid of no-js-warning
    document.getElementById("no-js-warning").remove();

    // top searchbar
    const search = document.getElementById("search");
    const clearSearch = document.getElementById("clear-search")

    search.addEventListener("input", () => {
        const recipeBoxes = document.querySelectorAll("div.recipebox");

        // grab search input value
        const searchText = search.value.toLowerCase().trim().normalize('NFD');
        const searchTerms = searchText.split(" ");
        let matchedRecipeBoxes = [];
        let unmatchedRecipeBoxes = [];

        // build lists of recipe boxes we have and haven't matched
        recipeBoxes.forEach(recipeBox => {
            const searchString = `${recipeBox.textContent} ${recipeBox.dataset.tags}`.toLowerCase().normalize('NFD');
            const isMatch = searchTerms.every(term => searchString.includes(term));

            if (isMatch) {
                matchedRecipeBoxes.push(recipeBox)
            } else {
                unmatchedRecipeBoxes.push(recipeBox)
            }
        })

        let columnsDivs = [];
        // build 3-wide "columns" divs for matched recipes
        const n_matches = matchedRecipeBoxes.length;
        for (let i = 0; i < n_matches; i += 3) {
            newColumnsDiv = document.createElement("div");
            newColumnsDiv.classList.add("columns");
            // this is a bit ugly, but it's more efficient than a
            // nested 'for' loop with a more generallized solution
            // because we know the width is just going to be 3 columns
            newColumnsDiv.appendChild(matchedRecipeBoxes[i]);
            if (i+1 < n_matches) {
                newColumnsDiv.appendChild(matchedRecipeBoxes[i+1]);
            }
            if (i+2 < n_matches) {
                newColumnsDiv.appendChild(matchedRecipeBoxes[i+2]);
            }
            columnsDivs.push(newColumnsDiv);
        }
        // throw all unmatched recipes into a single, invisible div
        hiddenDiv = document.createElement("div");
        hiddenDiv.classList.add("hidden");
        unmatchedRecipeBoxes.forEach(box => {hiddenDiv.appendChild(box)})

        const recipeSection = document.getElementById("recipesection");
        // destroy all of recipesection's current children (lmao)
        for (const child of recipeSection.children) {
            child.remove();
        }
        // rebuild recipesection with new children
        for (const columnDiv of columnsDivs) {
            recipeSection.appendChild(columnDiv);
        }
        recipeSection.appendChild(hiddenDiv);
    })

    document.querySelectorAll("#tagsection > div.tags > button").forEach(tag => {
        tag.addEventListener('click', () => {
            if (search.value == "") {
                search.value += tag.innerText + " ";
            } else {
                search.value += " " + tag.innerText;
            }
            search.dispatchEvent(new Event('input'));
        })
    })

    clearSearch.addEventListener("click", () => {
        search.value = "";
        search.dispatchEvent(new Event('input'));
    })
})
