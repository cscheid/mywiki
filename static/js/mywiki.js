// http://stackoverflow.com/questions/298750/how-do-i-select-text-nodes-with-jquery
function getTextNodesIn(el) {
    return $(el).find(":not(iframe)").andSelf().contents().filter(function() {
        return this.nodeType == 3;
    });
};

function wikify(selector, content) {
    // ugly:
    // we're going through the DOM every time here to avoid replacing attributes in the HTML text.
    $(selector).html(content);
    getTextNodesIn(selector).replaceWith(function(){
        //idx is the index of the current element in the JQUERY_OBJECT
        return this.data.replace(/\[\[(([A-Z]|[a-z]|[0-9])+)\]\]/g, "<a href='{{ prefix }}/view/$1'>$1</a>");
    });
    getTextNodesIn(selector).replaceWith(function(){
        //idx is the index of the current element in the JQUERY_OBJECT
        return this.data.replace(/\b(([A-Z]([0-9]|[a-z])+){2,})\b/g, "<a href='{{ prefix }}/view/$1'>$1</a>");
    });
}
