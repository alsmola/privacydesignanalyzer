function addResult(data) {
    if (data.indexOf('Error') == -1) {
        name = data.split(',')[0];
        parent = data.split(',')[1];
        var list = getList(parent);
        rowToUpdate = $(list).append(getItemHtml(name));
        $('.add-name').val('');
    } else {
        $('.error').html(data);
    }
}

function editResult(data) {
    if (data.indexOf('Error') == -1) {
        name = data.split(',')[0];
        newName = data.split(',')[1];
        parent = data.split(',')[2];
        rowToUpdate = getRow(name, parent);
        $(rowToUpdate).find('.update-name').val(newName);
        $(rowToUpdate).find('.name').text(newName);        
        $(rowToUpdate).find('.update-form').hide();
        $(rowToUpdate).find('.edit-delete').show();
    } else {
        $('.error').html(data);   
    }

}

function deleteResult(data) {
    if (data.indexOf('Error') == -1) {
        name = data.split(',')[0];
        parent = data.split(',')[1];
        row = getRow(name, parent);
        $(row).fadeOut();
        $(row).remove();
    } else {
        $('.error').html(data);  
    }
}

function getList(parent) {   
    var list = null;
    $('.response').each(function() {        
        var itemTypeAndParentName = $(this).find('.item-type-and-parent-name').val();
        if (itemTypeAndParentName.split(',')[0] == 'actor') {
            list = $(this).children('.list');
            
        }
        if (itemTypeAndParentName.split(',')[1] == parent) {
            list = $(this).children('.list');
        }        
    });
    return list;
}

function getRow(name, parent) {
    var row = null;
    var list = getList(parent);
    var children = $(list).children('li');
    $(children).each(function() {
        if ($(this).find('.name').text() == name) {
            row = this;
        }
    });
    return row;
}

function getItemHtml(name, itemType) {
    return '\
    <li>\
        <form class="update-form">\
            <input class="update-name" value="' + name + '">\
            <a class="update" href="#">Update</a>\
            <a class="cancel" href="#">Cancel</a>\
        </form>\
        <div class="edit-delete">\
            <span class="name">' + name + '</span>\
            <a class="edit" href="#">Edit</a>\
            <a class="delete" href="#">Delete</a>\
        </div>\
    </li>';
}

function error(thrownError) { 
    $('.error').html(thrownError);
}

$(document).ready(function () {
    
    $(".add").click(function() {
        var itemTypeAndParentName = $(this).parent().siblings('.item-type-and-parent-name').val();
        var itemType = itemTypeAndParentName.split(',')[0];
        var parentItemName = itemTypeAndParentName.split(',')[1];
        var itemName = $(this).siblings('.add-name').val();
        $.post('/' + itemType,
            { name : itemName, parent: parentItemName, verb: 'create' },
            function(data) {
                addResult(data, name);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
    });
    
    $('.delete').live('click', function () {
        var itemTypeAndParentName = $(this).parents('.list').siblings('.item-type-and-parent-name').val();
        var itemType = itemTypeAndParentName.split(',')[0];
        var parentItemName = itemTypeAndParentName.split(',')[1];
        var itemName = $(this).siblings('.name').text();
        $.post('/' + itemType, 
            { name : itemName, parent: parentItemName, verb: 'delete'},
            function(data) {
                deleteResult(data, itemName);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
    });
    
    $('.edit').live('click', function() {
        $(this).parent().hide();
        $(this).parent().siblings('.update-form').show();
    })
    
    $('.cancel').live('click', function() {
        $(this).parent().hide();
        $(this).parent().siblings('.edit-delete').show();
    })
    
    $('.update').live('click', function () {
        var itemTypeAndParentName = $(this).parents('.list').siblings('.item-type-and-parent-name').val();
        var itemType = itemTypeAndParentName.split(',')[0];
        var parentItemName = itemTypeAndParentName.split(',')[1];
        var name = $(this).parent().siblings('.edit-delete').children('.name').text();
        var newName = $(this).siblings('.update-name').val();
        if (name == newName) {
            $(this).parent().hide();
            $(this).parent().siblings('.edit-delete').show();
            return;
        }
        $.post('/' + itemType, 
            { name : name, newName: newName, parent: parentItemName, verb: 'edit'},
            function(data) {
                editResult(data, name);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
    });    
});