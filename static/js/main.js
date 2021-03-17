const categoriesDataBox = document.getElementById('categories-data-box')
const categoriesInput = document.getElementById('categories')

const featurenamesDataBox = document.getElementById('feature-names-data-box')
const featurenamesInput = document.getElementById('feature-names')

const categoryForm = document.getElementById('category-form')

const categoryText = document.getElementById('category-text')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const image_box = document.getElementById('thumbnail')
const allertBox = document.getElementById('allert-box')

const handleAlert = (type, text) => {
    allertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                            ${text}
                            </div>`
}

var list_of_feature_names = []

const url = ""

p_title = document.getElementById('id_title')
p_description = document.getElementById('id_description')
p_price = document.getElementById('id_price')
p_qty = document.getElementById('id_qty')
p_thumbnail = document.getElementById('id_thumbnail')

const image_url = ""

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


            })
        },
        error: function (error) {
            console.log(error)
        }
    })

})



p_thumbnail.addEventListener('change', ()=>{
    const image = p_thumbnail.files[0]
    const image_url = URL.createObjectURL(image)
    image_box.innerHTML = `<img src="${image_url}" width="100%">`
})

categoryForm.addEventListener('submit', e => {
    e.preventDefault()
    console.log('submitted')
    root = document.getElementById("feature-names-data-box")
    post_items = []
    p_title = document.getElementById('id_title')
    p_description = document.getElementById('id_description')
    p_price = document.getElementById('id_price')
    p_qty = document.getElementById('id_qty')
    p_thumbnail = document.getElementById('id_thumbnail')

    items = root.getElementsByClassName('item')
    for (index=0; index < items.length; index++){
        post_items.push(items[index].value)
    }
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('category', categoryText.textContent)
    fd.append('feature_names', list_of_feature_names.toString())
    fd.append('feature_values', post_items.toString())
    fd.append('title', p_title.value)
    fd.append('description', p_description.value)
    fd.append('price', p_price.value)
    fd.append('qty', p_qty.value)
    fd.append('thumbnail', p_thumbnail.files[0])

    $.ajax({
        type: "POST",
        url: '/create/',
        enctype: 'multipart/form-data',
        data: fd,
        success: function (response) {
            console.log(response)
            handleAlert("success", `You succesfully created new product. ${p_title.value} was created. You can back to the main page or create another one.`)
            setTimeout(()=>{
                allertBox.innerHTML = ""
                categoryText.innerHTML = "Select Category"
                featurenamesDataBox.innerHTML = ""
                p_title.value = ""
                p_description.value = ""
                p_price.value = ""
                p_qty.value = ""
                p_thumbnail.value = ""
            }, 2850)
        },
        error: function (error) {
            console.log(error)
            handleAlert('danger', "something went wrong")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

