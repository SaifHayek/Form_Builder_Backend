Front end 
Page 1 => Show all forms (This will show only the form titles that you created, once a user clicks on one of the forms, he will be moved to the creation form page where the form will be displayed and he can edit it)
Logically easy, but design needs time (1 day)

Page 2: Main Page Creation page (have 2 tabs, form builder and preview)
(2 day)
 
—--------------------------------------------------------------------------------------------------------------
APIs: 
1- Get Form /form/id ( will be used in the main creation and show form page)
2- Post /form to save a form 
3- update /form/ to update form. (note he can change the title name of the form)
4- Delete in the page 1 (provide a delete option)
5- Get Forms /forms
—----------------------------------------------------------------------------------------------------------------
Backend
database 
Table Name: Forms
Columns  [ id, Title_en, Title_ar, Fields [‘Json’]
Json:[
id:””
Type: ["text", "number", "email", "password", "checkbox", "select", "textarea", "radio" ]
Order: the order of the question.
Label_en: represents the question that the users will type
Label_ar: 
“Choices”: An array of choices for the dropdown { label: “, value: “, Id: “for you saif”}]
]

validation: {
    “required”: true,
    “minlength”: 5,
    “maxlength”: 10,
    "hide": false,
    "min_value": 1,
    "max_value": 10,
}


example: 

{
    title_en: "form_title",
    title_ar: "عنوان الفورم"
    fields: [
        {
            id: uuid,
            type: "text",
            order: 1,
            label_en: "What is your name?",
            label_ar: "ما هو اسمك",
            validation: {
                required: true,
                hide: true,
                min_length: 1,
                max_length: 2,
            }
        },
        {
            id: uuid,
            type: "select",
            order: 2,
            label_en: "Select your country",
            label_ar: "اختر بلدك",
            validation: {
                required: true,
                hide: true,     
            }
            choices: [
                {
                    label: "male",
                    value: "male",
                    id: random uuid
                },
                {
                    label: "female",
                    value: "female",
                    id: random uuid
                }
            ]
            
        }
    ]
}


Validations: 
On the form name: not empty, and its type string
On the Form structure (JSON):
Name: in  the following  [‘short text’, ‘drop-down’, ‘long text area’]
type: in one of the following  [‘text’, ‘dropdown’, ‘text area’]
Order: required, number, greater than 0.
Label: required, string



one of
9 days