import {KanbanController} from '@web/views/kanban/kanban_controller';
import {registry} from '@web/core/registry';
import {kanbanView} from '@web/views/kanban/kanban_view';
import {useService} from '@web/core/utils/hooks'

export class PassKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.orm = useService("orm");
    }
    async OnTestClick() {
        console.log("OnTestClick triggered");
        const task_ids = await this.orm.search("project.task", []);
        const result = await this.orm.call("project.task", "compute_something", [task_ids], {});
        console.log("result", result);
    }
}

registry.category("views").add("button_in_kanban", {
    ...kanbanView,
    Controller: PassKanbanController,
    buttonTemplate: "button_pass.view_sprint_week_kanban.Buttons",
});