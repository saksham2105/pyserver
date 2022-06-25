    var x;
    var count=0;
    var currentId=0;
    function deleteFromCart(menuItemId)
    {
    var f=document.getElementById("f");
    document.getElementById("menuItemId").value=menuItemId.toString();
    f.submit();
    }
    function addToCart(menuItemId,name,price,active,dateOfLaunch,category,freeDelievery)
    {
    var cartIdVal=1000;
    document.getElementById("cartId").value=cartIdVal.toString();
    document.getElementById("menuItemId").value=menuItemId.toString();
    document.getElementById("name").value=name;
    document.getElementById("price").value=price.toString();
    document.getElementById("active").value=active;
    document.getElementById("dateOfLaunch").value=dateOfLaunch;
    document.getElementById("category").value=category;
    document.getElementById("freeDelievery").value=freeDelievery;
    document.getElementById("divToTransparent").setAttribute("class","loading style-2");
    document.getElementById("wheelDiv").setAttribute("class","loading-wheel");
    x=setInterval(sendRequestToEdit,800);
    }
    function sendRequestToEdit()
    {
       if(count==2){
    count=0;
    document.getElementById("divToTransparent").removeAttribute("class","loading style-2");
    document.getElementById("wheelDiv").removeAttribute("class","loading-wheel");
    clearInterval(x);
    var frm=document.getElementById("frm");
    frm.submit();   
   } 
   else count+=1;
    
    }
    function resetBorder(id)
    {
    document.getElementById(id).removeAttribute("style","border:1px solid red");
    }
    function validateEditPage()
    {
    var name=document.getElementById("title").value;
    var price=document.getElementById("price").value;
    var active="";
    var flag=false;
    if(document.getElementById("active1").checked==true)
    {
    active="Yes";     
    }
    if(document.getElementById("active2").checked==true)
    {
    active="No";     
    }
    var dateOfLaunch=document.getElementById("dateOfLaunch").value;
    var category=document.getElementById("category").value;
    var freeDelievery="";
    var reg=/^[a-zA-Z ][a-zA-Z ]+[a-zA-Z]$/.test(name);
    if(document.getElementById("freeDelievery").checked==true) freeDelievery="Yes";
    else freeDelievery="No";
    if(name.trim()=="" || name.trim().length==0 || !reg)
    {
    flag=true;
    document.getElementById("title").value="";
    document.getElementById("title").setAttribute("style","border:1px solid red");
    }
    if(price<=0 || price.trim().length==0)
    {
    flag=true;
    document.getElementById("price").value="";
    document.getElementById("price").setAttribute("style","border:1px solid red");
    }
    if(dateOfLaunch.trim()=="" || dateOfLaunch.trim().length==0)
    {
    flag=true;
    document.getElementById("dateOfLaunch").value="";
    document.getElementById("price").setAttribute("style","border:1px solid red");
    }
    if(flag)
    {
    return;
    }
    else
    {
    var f=document.getElementById("f");
    document.getElementById("menuItemId").value=document.getElementById("itemId").value.toString();
    document.getElementById("nm").value=name;
    document.getElementById("prc").value=price.toString();
    document.getElementById("act").value=active;
    document.getElementById("dol").value=dateOfLaunch;
    document.getElementById("cat").value=category;
    document.getElementById("fd").value=freeDelievery;
    f.submit();
    }
    }
   function redirectToEdit(data)
   {
    currentId=data.toString();
    console.log(data);
    document.getElementById("divToTransparent").setAttribute("class","loading style-2");
    document.getElementById("wheelDiv").setAttribute("class","loading-wheel");
   x=setInterval(startTimer,600);
   } 
   function startTimer()
   {
   if(count==2){
    count=0;
    document.getElementById("divToTransparent").removeAttribute("class","loading style-2");
    document.getElementById("wheelDiv").removeAttribute("class","loading-wheel");
    clearInterval(x);
    var frm=document.getElementById("frm");
    document.getElementById("id").value= currentId;
    frm.submit();   
   } 
   else count+=1;
   }
