function login(){
    var email= document.getElementById('email').value
    var password=document.getElementById('password').value
    var csrf= document.getElementById('csrf').value

    if(email=='' && password==''){
        alert('enter email and password')
    }
    var data={
        'email':email,
        'password':password
    }
    fetch('/api/login',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrf,
        },
        body :JSON.stringify(data)
    }).then(result=>result.json())
    .then(response=>{
        if (response.status==200){
            window.location.href='/'
        }
        else{
            alert(response.message)
        }
    })
}

// register
function register(){
    var username= document.getElementById('username').value
    var email= document.getElementById('email').value
    var password=document.getElementById('password').value
    var csrf= document.getElementById('csrf').value

    if(username=='' && email=='' && password==''){
        alert('enter username and password')
    }

    var data={
        'username':username,
        'email':email,
        'password':password
    }

    fetch('/api/register',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrf,
        },
        body :JSON.stringify(data)
    }).then(result=>result.json())
    .then(response=>{
        if (response.status==200){
            window.location.href='/login'
        }
        else{
            alert(response.message)
        }
    })
    
}


// button for detail
function buttons(){
    const detailbtn = document.getElementById('detailbtn')
    if (detailbtn) {
        detailbtn.onclick=()=>{
        blogdetail(detailbtn.value)  
    }}
    
    // button for update
    var update=document.getElementById('update')
    if (update){
    update.onclick=()=>{
        updateblog(update.value)
    }}
    }
buttons()

var blogtable = document.querySelector(".blog-table")
window.onload=()=>{
    listview()
    bloglist()
}

// addBlog
function addBlog(){
    var title= document.getElementById('title').value
    var content= document.getElementById('content').value
    var image=document.querySelector('#image').files[0]
    var csrf= document.getElementById('csrf').value
    console.log(title)
    var data={
        'title':title,
        'content':content,
        'image':image
    }
    console.log(data['image'])
    fetch('/api/addblog',{
        method:'POST',
        headers:{
            'Accept': 'multipart/form-data',
            'Content-Type':'application/json',            
            'X-CSRFToken':csrf,
        },
        body:JSON.stringify(data)
    }).then(result=>result.json())
    .then(response=>{
        if (response.status==200){
            window.location.href='/'
        }
        else{
            alert(response.message)
        }
    })
}

// list of blog in home page
function listview(){
    fetch('/view',{
    method:'GET',
    headers:{
        'Content-Type':'application/json'
    },
    body :JSON.stringify()
    }).then(response=>response.json())
    .then(result=>{
        blogs=result
        for (var blog in blogs){
                showlist(blogs[blog])
            }
        })
    }
var coursesContainer = document.querySelector(".blog-container")
function showlist(blog){ 
        const card = document.createElement("div");
        card.classList.add("card");
      
        const a = document.createElement("div");
        a.classList.add("card-content");
      
        const img = document.createElement("img");
        img.setAttribute("src",`/static/img/${blog.image}`);
      
        var title = document.createElement("a");
        title.classList.add("title");
        // title.setAttribute("href",`blogdetail/${blog.slug}`);
        title.innerHTML=blog.title
    
        const author = document.createElement("div");
        author.classList.add("author");
        author.innerHTML = blog.user_id;
      
        const readmore = document.createElement("a");
        readmore.classList.add("readmore");
        readmore.setAttribute("href",`blogdetail/${blog.slug}`);      
        readmore.innerHTML = `Read More`;
      
        const updated_at = document.createElement("div");
        updated_at.classList.add("updated");
        updated_at.innerHTML = blog.updated_at;
      
        coursesContainer.appendChild(card);
        card.appendChild(a);
        a.appendChild(img);
        a.appendChild(title);
        a.appendChild(author);              
        a.appendChild(readmore);   
        a.appendChild(updated_at);    
      
}

//blog list in view your blog
function bloglist(){
    fetch(`/api/listblog`,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
        },
        body :JSON.stringify()
    }).then(response=>response.json())
    .then(data=>{
        blogs=data   
        for (var blog of blogs){
                tableblog(blog)
            }
        })
}

function tableblog(blog){      
    var rows = "";
    var id = blog.id;
    var title= blog.title;
    var created_at=blog.created_at;

    var actionedi=document.createElement("td")
    var edi = document.createElement("a");
    edi.setAttribute("href",`updateblog/${blog.slug}` );
    edi.innerHTML = 'Edit'; 

    var actiondel=document.createElement("td")
    var del= document.createElement("button");
    del.innerHTML = 'Delete';
    del.onclick=()=>{blogdelete(blog.slug)}   

    rows += "<tr><td>" + id + "</td><td>" + title + "</td><td>" + created_at + "</td></tr>";
    var tbody = document.querySelector("#list tbody");
    var tr = document.createElement("tr");

    tr.innerHTML = rows;
    tr.appendChild(actionedi);
    actionedi.appendChild(edi);
    tr.appendChild(actiondel);
    actiondel.appendChild(del);
    tbody.appendChild(tr);
}


//blog update
function updateblog(slug){
    var slug=slug
    var title= document.getElementById('title').value
    var content= document.getElementById('content').value
    var image=document.querySelector('#image').files[0]
    var csrf= document.getElementById('csrf').value
    console.log(title)
    var data={
        'title':title,
        'content':content,
        'image':image
    }
    console.log(data['image'])
    fetch(`/api/updateblog/${slug}`,{
        method:'PUT',
        headers:{
            'Accept': 'multipart/form-data',
            'Content-Type':'application/json',            
            'X-CSRFToken':csrf,
        },
        body:JSON.stringify(data)
    }).then(result=>result.json())
    .then(response=>{
        if (response.status==200){
            content=response
            console.log(content)
            window.location.href='/'
        }
        else{
            alert(response.message)
        }
    })
    
}




// for blog detail page
function blogdetail(slug){    
    var slug=slug
    console.log(slug)
    fetch(`/api/blogdetail/${slug}`,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            // 'X-CSRFToken':csrf,
        },
        body :JSON.stringify()
    }).then(response=>response.json())
    .then(data=>{
        blogs=data
        viewdetail(blogs)})

}

function viewdetail(blog){
    console.log(blog.slug)    
    var title=document.getElementById('title')
    var img=document.getElementById('detail-img')
    var content=document.getElementById('content')
    var author=document.getElementById('author')
    
    console.log(blog.title)
    title.innerHTML=blog.title
    img.setAttribute("src",`/static/img/${blog.image}`)
    content.innerHTML=blog.content
    author.innerHTML = blog.user_id
    
}
 

//blog delete 
function blogdelete(slug){
    var csrf= document.getElementById('csrf').value
    var slug = slug
    console.log(slug)
    fetch(`/api/blogdelete/${slug}`,{
        method:'DELETE',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrf,
        },
        body :JSON.stringify()
    }).then(result=>result.json())
    .then(response=>{
        console.log(response)
        window.location.href='/listblog'
})
}

