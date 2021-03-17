const categoriesDataBox = document.getElementById('categories-data-box')
const categoriesInput = document.getElementById('categories')

const featurenamesDataBox = document.getElementById('feature-names-data-box')
const featurenamesInput = document.getElementById('feature-names')



const categoryForm = document.getElementById('category-form')


const categoryText = document.getElementById('category-text')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

var list_of_feature_id = []

$.ajax({
    type: 'GET',
    url: '/categories-json/',
    success: function (response){
        console.log(response.data)
        const categoriesData = response.data;
        categoriesData.map(item =>{
            const option = document.createElement('div');
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            categoriesDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})

categoriesInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedCategory = e.target.value

    featurenamesDataBox.innerHTML = ""

    $.ajax({
        type: "GET",
        url: `/feature-name-json/${selectedCategory}/`,
        success: function(response){
            console.log(response.data)
            const featurenamesData = response.data
            featurenamesData.map(item =>{
                const option2 = document.createElement('label');
                const option = document.createElement('input');
                option2.textContent = item.feature_name
                option.setAttribute('class', 'item')
                option.setAttribute('type', 'text')
                option.setAttribute('name', item.feature_name)
                option.setAttribute('placeholder', item.feature_name)
                console.log(featurenamesDataBox)
                featurenamesDataBox.appendChild(option2)
                featurenamesDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })

})  



categoryForm.addEventListener('submit', e =>{
    console.log(e.target.value)
    e.preventDefault()
    console.log(e)
    console.log('submitted')
    $.ajax({
        type: "POST",
        url:'/create/',
        data:{
            'csrfmiddlewaretoken': csrf[0].value,
            'category': categoryText.textContent,
            'feature_name': 'list_of_names',
        },
        success: function(response){
            console.log(response)
            console.log(list_of_feature_id)
        },
        error: function(error){
            console.log(error)
        }

    })
})