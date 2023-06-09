/*
  NOTE snippet from based.cooking, which I am shamelessly ripping off here
document.addEventListener("DOMContentLoaded", () => {
  for (e of document.getElementsByClassName("js-only")) {
    e.classList.remove("js-only");
  }

  const recipes = document.querySelectorAll("#artlist li");
  const search = document.getElementById("search");
  const oldheading = document.getElementById("newest-recipes");
  const clearSearch = document.getElementById("clear-search");
  const artlist = document.getElementById("artlist");

  search.addEventListener("input", () => {
    // grab search input value
    const searchText = search.value.toLowerCase().trim().normalize('NFD').replace(/\p{Diacritic}/gu, "");
    const searchTerms = searchText.split(" ");
    const hasFilter = searchText.length > 0;

    artlist.classList.toggle("list-searched", hasFilter);
    oldheading.classList.toggle("hidden", hasFilter);

    // for each recipe hide all but matched
    recipes.forEach(recipe => {
      const searchString = `${recipe.textContent} ${recipe.dataset.tags}`.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, "");
      const isMatch = searchTerms.every(term => searchString.includes(term));

      recipe.hidden = !isMatch;
      recipe.classList.toggle("matched-recipe", hasFilter && isMatch);
    })
  })

  clearSearch.addEventListener("click", () => {
    search.value = "";
    recipes.forEach(recipe => {
      recipe.hidden = false;
      recipe.classList.remove("matched-recipe");
    })

    artlist.classList.remove("list-searched");
    oldheading.classList.remove("hidden");
  })
})
*/

document.addEventListener("DOMContentLoaded", () => {
    // we're clearly running javascript, so get rid of no-js-warning
    document.getElementById("no-js-warning").remove();

    search.addEventListener("input", () => {
        const recipeBoxes = document.querySelectorAll("div.recipebox");
        const search = document.getElementById("search");

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
})
