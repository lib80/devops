package org.devops

def dingding_notify(mobile_num) {
    dingtalk (
        robot: 'xxx',
        type: 'MARKDOWN',
        text: [
            "${currentBuild.fullProjectName}",
            "",
            "---",
            "- 任务：${currentBuild.number}",
            "- 状态：${currentBuild.result}",
            "- 持续时间：${currentBuild.durationString}",
            "- 动作：${params.action}",
            "- 分支/commitId：${src_branch}",
            "- 执行人：${executor}",
            "- build-url: ${env.BUILD_URL}"
        ],
        at: [mobile_num]
    )
}
