import { KanbanController } from '@web/views/kanban/kanban_controller';
import { registry } from '@web/core/registry';
import { kanbanView } from '@web/views/kanban/kanban_view';

export class KanbanController extends KanbanController {
    setup() {
        super.setup();
    }
    OnTestClick() {

    }
}
registry.category("views").add("button_in_kanban", {
    ...KanbanView,
    Controller: SaleKanbanController,
    buttonTemplate: "button_pass.KanbanView.Buttons",
});