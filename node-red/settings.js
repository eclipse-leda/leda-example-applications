/*
 * This is a customized settings file for the SDV Node-RED example.
 */

module.exports = {
    editorTheme: {
        functionExternalModules: true,
        theme: "midnight-red",
        palette: {
            /** The following property can be used to order the categories in the editor
             * palette. If a node's category is not in the list, the category will get
             * added to the end of the palette.
             * If not set, the following default order is used:
             */
            categories: ['SDV', 'subflows', 'common', 'function', 'network', 'sequence', 'parser', 'storage'],
        },
        projects: {
            enabled: true,
            workflow: {
                mode: "manual"
            }
        }
    }
}
