$(function() {
    load();

    // 添加任务
    $('#title').on('keyup', function(e) {
        if (e.keyCode === 13) {
            var content = $(this).val().trim();
            if (content) {
                var data = getData();
                data.push({
                    'title': content,
                    'done': false
                });
                saveData(data);
                load();
            } else {
                alert('请输入内容');
            }
            $(this).val('');
        }
    })

    // 删除任务
    $('ul, ol').on('click', 'a', function() {
        var data = getData()
        data.splice($(this).prop('id'), 1);
        saveData(data);
        load();
    })

    // 更改任务状态
    $('ul, ol').on('click', 'input', function() {
        var data = getData();
        data[$(this).siblings('a').prop('id')].done = $(this).prop('checked');
        saveData(data)
        load();
    })

    function saveData(data) {
        localStorage.setItem('todolist', JSON.stringify(data));
    }

    function getData() {
        var data = localStorage.getItem('todolist');
        if (data === null) {
            data = []
        } else {
            data = JSON.parse(data)
        }
        return data
    }

    function load() {
        $('ul, ol').empty();
        var todoCount = 0;
        var doneCount = 0;
        var data = getData();
        $.each(data, function(i, e) {
            if (e.done) {
                // 已完成
                $('ul').prepend($('<li><input type="checkbox" checked="checked"><p>' + e.title + '</p><a href="javascript:;" id=' + i + '></a></li>'));
                doneCount++;
            } else {
                // 未完成
                $('ol').prepend($('<li><input type="checkbox"><p>' + e.title + '</p><a href="javascript:;" id=' + i + '></a></li>'));
                todoCount++;
            }
        })
        $('#todocount').text(todoCount);
        $('#donecount').text(doneCount);
    }
})
