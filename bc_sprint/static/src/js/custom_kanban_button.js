import { KanbanController } from '@web/views/kanban/kanban_controller';
import { registry } from '@web/core/registry';
import { kanbanView } from '@web/views/kanban/kanban_view';

export class PassKanbanController extends KanbanController {
    setup() {
        super.setup();
    }
    OnTestClick() {
        console.log('test');
    }
}
registry.category("views").add("button_in_kanban", {
    ...kanbanView,
    Controller: PassKanbanController,
    buttonTemplate: "button_pass.view_sprint_week_kanban.Buttons",
});