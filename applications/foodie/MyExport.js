function foo() {
    alert("I got clicked");
}
function MyExport() {
   const buttonText = "Click Me :)"; 
   return(
    <div>
    <h1>Online React Tutorial</h1>
    <span>Learn More</span>
    <button onClick={foo}>
     {buttonText}
    </button>
    </div>
   );
}
export default MyExport;