const categoriesDataBox = document.getElementById('categories-data-box')
const categoriesInput = document.getElementById('categories')

const featurenamesDataBox = document.getElementById('feature-names-data-box')
const featurenamesInput = document.getElementById('feature-names')

const categoryForm = document.getElementById('category-form')

const categoryText = document.getElementById('category-text')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

var list_of_feature_names = []

$.ajax({
    type: 'GET',
    url: '/categories-json/',
    success: function (response) {

        console.log('success', response.data)

        const categoriesData = response.data;
        categoriesData.map(item => {
            const option = document.createElement('div');
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            categoriesDataBox.appendChild(option)
        })
    },
    error: function (error) {
        console.log(error)
    }
})

categoriesInput.addEventListener('change', e => {
    console.log(e.target.value)
    const selectedCategory = e.target.value

    featurenamesDataBox.innerHTML = ""

    $.ajax({
        type: "GET",
        url: `/feature-name-json/${selectedCategory}/`,
        success: function (response) {
            console.log(response.data)
            const featurenamesData = response.data
            console.log('featurenamesData', featurenamesData)

            featurenamesData.map(item => {
                const option2 = document.createElement('label');
                const option = document.createElement('input');
                option2.textContent = item.feature_name
                option.setAttribute('class', 'item')
                option.setAttribute('type', 'text')
                option.setAttribute('name', item.feature_name)
                option.setAttribute('placeholder', item.feature_name)
                option.setAttribute('id', item.id)
                option.setAttribute('data-category-id', item.category_id)
                list_of_feature_names.push(item.feature_name)
                featurenamesDataBox.appendChild(option2)
                featurenamesDataBox.appendChild(option)

                // console.log('featurenamesDataBox', featurenamesDataBox)
            })



        },
        error: function (error) {
            console.log(error)
        }
    })

})


categoryForm.addEventListener('submit', e => {
    e.preventDefault()
    console.log('submitted')

    root = document.getElementById("feature-names-data-box")

    post_items = []

    items = root.getElementsByClassName('item')
    for (index=0; index < items.length; index++){
        post_items.push(items[index].value)
    }


    $.ajax({
        type: "POST",
        url: '/create/',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'category': categoryText.textContent,
            'feature_names': list_of_feature_names.toString(),
            'feature_values': post_items.toString(),
        },
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log(error)
        }

    })
})