import {KanbanController} from '@web/views/kanban/kanban_controller';
import {registry} from '@web/core/registry';
import {kanbanView} from '@web/views/kanban/kanban_view';
import {useService} from '@web/core/utils/hooks';
import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';

export class PassKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.dialog = useService("dialog");
    }

    async OnTestClick() {
        this.dialog.add(ConfirmationDialog, {
            title: "Confirmation de l'action",
            body: "Souhaitez-vous vraiment passer la semaine?",
            confirmLabel: "Oui, Confirmer",
            confirm: async (context) => {
                const task_ids = await this.orm.search("project.task", []);
                await this.orm.call("project.task", "compute_something", [task_ids], {});
                location.reload();
            },
        });
    }
}

registry.category("views").add("button_in_kanban", {
    ...kanbanView,
    Controller: PassKanbanController,
    buttonTemplate: "button_pass.view_sprint_week_kanban.Buttons",
});