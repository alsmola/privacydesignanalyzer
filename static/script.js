function addResult(result) {
    if (result['success']) {
        if (result['parent_type'] == 'none') {
            $('#applications').append(getItemHtml(result['name'], result['type'], result['id'])).fadeIn();
        } else {
            $('#' + result['parent_type'] + '-' + result['parent_id']).append(getItemHtml(result['name'], result['type'], result['id'])).fadeIn();
        }
        $('.add-name').val('');
    } else {
        $('.error').html(result['message']);
    }
}

function editResult(result) {
    if (result['success']) {
        rowToUpdate = $('#' + result['type'] + '-' + result['id']);
        $(rowToUpdate).find('.update-name').val(result['name']);
        $(rowToUpdate).find('.name').text(result['name']);        
        $(rowToUpdate).find('.update-form').hide();
        $(rowToUpdate).find('.edit-delete').fadeIn('slow');
    } else {
        $('.error').html(result['message']);
    }

}

function deleteResult(result) {
    if (result['success']) {
        rowToDelete = $('#' + result['type'] + '-' + result['id']);
        $(rowToDelete).fadeOut();
    } else {
        $('.error').html(result['message']);
    }
}

function getItemHtml(name, type, id) {
    html = '\
    <li class="item" id="' + type + '-' + id + '">\
        <form class="update-form">\
            <input class="update-name" value="' + name + '"/>\
            <a class="update" href="#">Update</a>\
            <a class="cancel" href="#">Cancel</a>\
            <div class="clear"></div>\
        </form>\
        <div class="edit-delete">'
    if (type == 'application') {
        html += '<a href="actors?app_id=' + id + '"><span class="name">' + name + '</span></a>'
    } else {
        html += '<p class="name">' + name + '</p>'
    }
    html += '\
            <a class="edit" href="#">Edit</a>\
            <a class="delete" href="#">Delete</a>\
            <div class="clear"></div>\
        </div>\
    </li>'
    return html;
}

function error(thrownError) { 
    $('.error').html(thrownError);
}

$(document).ready(function () {   
    if ($('#app-name').text() == '- ') {
        $('#app-name').hide();
    }
    $('.add-form').submit(function(event) {
        event.preventDefault();
        var name = $(this).children('.add-name').val();
        var parentId = $(this).siblings('.list').attr('id').split('-')[1];
        var type = $(this).children('.type').val();
        $.post(type,
            { name : name, verb: 'create', id: -1, parent_id: parentId},
            function(data) {
                addResult(data);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
        return false;
    });
    
    $('.add').click(function() {
        $(this).parents('.add-form').submit();
    });
    
    $('.delete').live('click', function () {
        var name = $(this).siblings('.name').text();
        var type = $(this).parents('.item').attr('id').split('-')[0];
        var id = $(this).parents('.item').attr('id').split('-')[1];
        var parentId = $(this).parents('.list').attr('id').split('-')[1];
        $.post(type, 
            { name : name, verb: 'delete', id: id, parent_id: parentId},
            function(data) {
                deleteResult(data);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
        return false;
    });
    
    $('.edit').live('click', function() {
        $(this).parent().hide();
        $(this).parent().siblings('.update-form').fadeIn();
        return false;
    });
    
    $('.cancel').live('click', function() {
        $(this).parent().hide();
        $(this).parent().siblings('.edit-delete').fadeIn();
        return false;
    });
    
    $('.update-form').live('submit', function(event) {
        event.preventDefault();
        var name = $(this).siblings('.edit-delete').children('.name').text();
        var newName = $(this).children('.update-name').val();
        var type = $(this).parents('.item').attr('id').split('-')[0];
        var id = $(this).parents('.item').attr('id').split('-')[1];
        var parentId = $(this).parents('.list').attr('id').split('-')[1];
        if (name == newName) {
            $(this).parent().hide();
            $(this).parent().siblings('.edit-delete').fadeIn();
            return false;
        }
        $.post(type, 
            { name : name, newName: newName, verb: 'edit', id: id, parent_id: parentId},
            function(data) {
                editResult(data);
            }
        ).error(function(xhr, ajaxOptions, thrownError) { error(thrownError) } );
        return false;
    });
    
    $('.update').live('click', function () {
        $(this).parents('.update-form').submit();
        return false;
    });
    
    
    $('.select-all').live('click', function() {
        $(this).siblings('.choice').find('input').attr('checked', 'true');
       return false; 
    });
    
    $('.select-none').live('click', function() {
        $(this).siblings('.choice').find('input').removeAttr('checked');
       return false; 
    });
    
});