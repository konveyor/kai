from dataclasses import dataclass, field
from typing import Any, Self

import tree_sitter as ts

from .base import DiffableDict, DiffableSummary


@dataclass
class JAnnotation(DiffableSummary):
    name: str
    params: str

    def __hash__(self) -> int:
        return hash(f"{self.name}")

    def equal(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return self.name == o.name and self.params == o.params
        return False

    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name}
        if self.params:
            d["parameters"] = self.params
        return d

    def diff(self, o: Self) -> dict[str, Any]:
        diff: dict[str, Any] = {}
        if self == o:
            return diff
        if self.params != o.params:
            diff["params"] = {
                "old": self.params,
                "new": o.params,
            }
        return diff


@dataclass
class JVariable(DiffableSummary):
    name: str
    typ: str
    annotations: DiffableDict

    def __hash__(self) -> int:
        return hash(f"{self.name}{self.typ}")

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return (
                self.name == o.name
                and self.typ == o.typ
                and self.annotations == o.annotations
            )
        return False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "type": self.typ,
        }
        if self.annotations:
            d["annotations"] = list(self.annotations)
        return d

    def diff(self, o: Self) -> dict[str, Any]:
        diff = {}
        if self.typ != o.typ:
            diff["type"] = {
                "old": self.typ,
                "new": o.typ,
            }
        if self.annotations != o.annotations:
            diff["annotations"] = self.annotations.diff(o.annotations)
        return diff


@dataclass
class JMethod(DiffableSummary):
    name: str
    annotations: DiffableDict
    parameters: str = ""
    return_type: str = ""
    body: str = ""

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return (
                o.name == self.name
                and o.parameters == self.parameters
                and self.return_type == o.return_type
                and self.body == o.body
                and self.annotations == o.annotations
            )
        return False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"name": self.name}
        if self.parameters:
            d["parameters"] = self.parameters
        if self.return_type:
            d["return_type"] = self.return_type
        if self.body:
            d["body"] = self.body
        if self.annotations:
            d["annotations"] = list(self.annotations)
        return d

    def diff(self, o: Self) -> dict[str, Any]:
        diff: dict[str, Any] = {}
        if self == o:
            return diff
        diff["name"] = self.name
        if self.parameters != o.parameters:
            diff["parameters"] = {
                "old": self.parameters,
                "new": o.parameters,
            }
        if self.return_type != o.return_type:
            diff["return_type"] = {
                "old": self.return_type,
                "new": o.return_type,
            }
        else:
            diff["return_type"] = self.return_type
        if self.body != o.body:
            diff["body"] = {
                "old": self.body,
                "new": o.body,
            }
        else:
            diff["body"] = self.body
        if self.annotations != o.annotations:
            diff["annotations"] = self.annotations.diff(o.annotations)
        else:
            diff["annotations"] = list(self.annotations)
        return diff


@dataclass
class JClass(DiffableSummary):
    name: str
    super_class: str
    fields: DiffableDict
    methods: DiffableDict
    annotations: DiffableDict
    interfaces: set[str] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return (
                self.name == o.name
                and self.super_class == o.super_class
                and self.fields == o.fields
                and self.methods == o.methods
                and self.interfaces == o.interfaces
                and self.annotations == o.annotations
            )
        return False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"name": self.name}
        if self.super_class:
            d["super_class"] = self.super_class
        if self.interfaces:
            d["interfaces"] = list(self.interfaces)
        if self.annotations:
            d["annotations"] = list(self.annotations)
        if self.fields:
            d["fields"] = self.fields.to_dict()
        if self.methods:
            d["methods"] = self.methods.to_dict()
        return d

    def diff(self, o: Self) -> dict[str, Any]:
        diff: dict[str, Any] = {"name": self.name}
        if self.super_class != o.super_class:
            diff["super_class"] = {
                "old": self.super_class,
                "new": o.super_class,
            }
        if self.interfaces != o.interfaces:
            diff["interfaces"] = {
                "old": list(self.interfaces),
                "new": list(o.interfaces),
            }
        if self.fields != o.fields:
            diff["fields"] = self.fields.diff(o.fields)
        else:
            diff["fields"] = list(self.fields)
        if self.methods != o.methods:
            diff["methods"] = self.methods.diff(o.methods)
        else:
            diff["methods"] = list(self.methods)
        if self.annotations != o.annotations:
            diff["annotations"] = self.annotations.diff(o.annotations)
        else:
            diff["annotations"] = list(self.annotations)
        return diff


@dataclass
class JFile(DiffableSummary):
    classes: DiffableDict
    imports: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.classes:
            d["classes"] = self.classes.to_dict()
        if self.imports:
            d["imports"] = list(self.imports)
        return d

    def diff(self, o: Self) -> dict[str, Any]:
        diff: dict[str, Any] = {}
        if self.imports != o.imports:
            diff["imports"] = {
                "old": list(self.imports),
                "new": list(o.imports),
            }
        if self.classes != o.classes:
            diff["classes"] = self.classes.diff(o.classes)
        else:
            diff["classes"] = list(self.classes)
        return diff


def _extract_java_info(root: ts.Node) -> DiffableSummary:
    cursor = root.walk()

    def traverse(node: ts.Node) -> DiffableSummary:
        match node.type:
            case "modifiers":
                annotations = DiffableDict[str, JAnnotation]()
                for child in node.children:
                    match child.type:
                        case "marker_annotation" | "annotation":
                            annotation_name = ""
                            params = ""
                            for annotation_child in child.children:
                                match annotation_child.type:
                                    case "identifier":
                                        if annotation_child.text is None:
                                            raise ValueError(
                                                "Annotation identifier has no text"
                                            )

                                        annotation_name = annotation_child.text.decode(
                                            "utf-8"
                                        )
                                    case "annotation_argument_list":
                                        if annotation_child.text is None:
                                            raise ValueError(
                                                "Annotation argument list has no text"
                                            )

                                        params = (
                                            annotation_child.text.decode("utf-8")
                                            .replace("\\n", "", -1)
                                            .replace("\\t", "", -1)
                                        )
                            annotation = JAnnotation(annotation_name, params)
                            annotations[str(hash(annotation))] = annotation
                return annotations
            case "field_declaration":
                name = ""
                type = ""
                annotations = DiffableDict[str, JAnnotation]()
                for field_child in node.children:
                    match field_child.type:
                        case "type_identifier" | "generic_type":
                            if field_child.text is None:
                                raise ValueError("Field type has no text")

                            type = field_child.text.decode("utf-8")

                        case "variable_declarator":
                            for var_child in field_child.children:
                                if var_child.text is None:
                                    raise ValueError("Variable declarator has no text")

                                if var_child.type == "identifier":
                                    name = var_child.text.decode("utf-8")

                        case "modifiers":
                            field_child_info = traverse(field_child)
                            if isinstance(field_child_info, DiffableDict):
                                annotations = field_child_info
                return JVariable(name=name, typ=type, annotations=annotations)
            case "method_declaration":
                name = ""
                body = ""
                params = ""
                annotations = DiffableDict[str, JAnnotation]()
                for mt_child in node.children:
                    match mt_child.type:
                        case "identifier":
                            if mt_child.text is None:
                                raise ValueError("Method identifier has no text")

                            name = mt_child.text.decode("utf-8")

                        case "modifiers":
                            anns = traverse(mt_child)
                            if isinstance(anns, DiffableDict):
                                annotations = anns

                        case "formal_parameters":
                            if mt_child.text is None:
                                raise ValueError("Method parameters have no text")

                            params = mt_child.text.decode("utf-8")

                        case "block":
                            if mt_child.text is None:
                                raise ValueError("Method block has no text")

                            body = (
                                mt_child.text.decode("utf-8")
                                .strip()
                                .replace("\\n", "", -1)
                                .replace("\\t", "", -1)
                            )
                return JMethod(
                    name=name, annotations=annotations, body=body, parameters=params
                )
            case "class_declaration":
                name = ""
                fields = DiffableDict[str, JVariable]()
                methods = DiffableDict[str, JMethod]()
                interfaces: set[str] = set()
                super_class: str = ""
                annotations = DiffableDict[str, JAnnotation]()

                for class_child in node.children:
                    match class_child.type:
                        case "modifiers":
                            mods = traverse(class_child)
                            if isinstance(mods, DiffableDict):
                                annotations = mods
                        case "identifier":
                            if class_child.text is None:
                                raise ValueError("Class identifier has no text")

                            name = class_child.text.decode("utf-8")
                        case "superclass":
                            if class_child.text is None:
                                raise ValueError("Superclass has no text")

                            super_class = class_child.text.decode("utf-8")
                        case "super_interfaces":
                            interfaces = set()

                            for i in class_child.children:
                                if i.type != "," and i.text is not None:
                                    interfaces.add(i.text.decode("utf-8"))

                        case "class_body":
                            for cb_child in class_child.children:
                                match cb_child.type:
                                    case "field_declaration" | "method_declaration":
                                        cb_info = traverse(cb_child)
                                        match cb_info:
                                            case cb_info if isinstance(
                                                cb_info, JVariable
                                            ):
                                                fields[str(hash(cb_info))] = cb_info
                                            case cb_info if isinstance(
                                                cb_info, JMethod
                                            ):
                                                methods[str(hash(cb_info))] = cb_info
                return JClass(
                    name=name,
                    fields=fields,
                    methods=methods,
                    annotations=annotations,
                    interfaces=interfaces,
                    super_class=super_class,
                )

        classes = DiffableDict[str, DiffableSummary]()
        imports = set()
        for child in node.children:
            match child.type:
                case "import_declaration":
                    if child.text is None:
                        raise ValueError("Import declaration has no text")

                    imports.add(
                        child.text.decode("utf-8")
                        .replace("import ", "", -1)
                        .rstrip(";")
                    )
                case _:
                    cb_info = traverse(child)
                    if isinstance(cb_info, JClass):
                        classes[cb_info.name] = cb_info
        return JFile(classes=classes, imports=imports)

    if cursor.node is None:
        return DiffableDict()

    return traverse(cursor.node)
