# -*- coding: utf-8 -*-

import os
import sys


def fix_customtkinter_scaling_zero_bug():
    try:
        import customtkinter as ctk

        try:
            ctk.deactivate_automatic_dpi_awareness()
        except Exception:
            pass

        try:
            ctk.set_widget_scaling(1.0)
            ctk.set_window_scaling(1.0)
        except Exception:
            pass

        try:
            from customtkinter.windows.widgets.scaling.scaling_base_class import CTkScalingBaseClass

            original_set_scaling = getattr(CTkScalingBaseClass, "_set_scaling", None)

            def safe_float(value, default=1.0):
                try:
                    result = float(value)
                except Exception:
                    return default

                if result <= 0:
                    return default

                return result

            if original_set_scaling:
                def safe_set_scaling(self, *args, **kwargs):
                    safe_args = list(args)

                    if len(safe_args) >= 1:
                        safe_args[0] = safe_float(safe_args[0], 1.0)

                    if len(safe_args) >= 2:
                        safe_args[1] = safe_float(safe_args[1], 1.0)

                    if "new_widget_scaling" in kwargs:
                        kwargs["new_widget_scaling"] = safe_float(
                            kwargs["new_widget_scaling"],
                            1.0,
                        )

                    if "new_window_scaling" in kwargs:
                        kwargs["new_window_scaling"] = safe_float(
                            kwargs["new_window_scaling"],
                            1.0,
                        )

                    return original_set_scaling(self, *safe_args, **kwargs)

                CTkScalingBaseClass._set_scaling = safe_set_scaling

            def safe_reverse_window_scaling(self, scaled_value):
                scaling = safe_float(
                    getattr(self, "_CTkScalingBaseClass__window_scaling", 1.0),
                    1.0,
                )

                try:
                    setattr(self, "_CTkScalingBaseClass__window_scaling", scaling)
                except Exception:
                    pass

                try:
                    return int(scaled_value / scaling)
                except Exception:
                    return int(scaled_value)

            def safe_apply_window_scaling(self, value):
                scaling = safe_float(
                    getattr(self, "_CTkScalingBaseClass__window_scaling", 1.0),
                    1.0,
                )

                try:
                    setattr(self, "_CTkScalingBaseClass__window_scaling", scaling)
                except Exception:
                    pass

                try:
                    if isinstance(value, int):
                        return int(value * scaling)

                    return value * scaling
                except Exception:
                    return value

            CTkScalingBaseClass._reverse_window_scaling = safe_reverse_window_scaling
            CTkScalingBaseClass._apply_window_scaling = safe_apply_window_scaling

            print("✅ CustomTkinter scaling 安全修正已啟用")

        except Exception as e:
            print(f"⚠️ CustomTkinter scaling monkey patch 未套用: {e}")

    except Exception as e:
        print(f"⚠️ CustomTkinter scaling 修正初始化失敗: {e}")


fix_customtkinter_scaling_zero_bug()

from app.gui.main_app import MainApp


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()