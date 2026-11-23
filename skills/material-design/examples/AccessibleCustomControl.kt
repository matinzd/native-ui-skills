// AccessibleCustomControl.kt
//
// Purpose: two custom controls built from foundation modifiers with complete semantics: a
// favorite toggle and a five-star rating. Each has a role, a label, a spoken state, a 48dp
// minimum interactive size, and a state cue that does not depend on color.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x; foundation and ui 1.13. Nothing
//   here is newer than material3 1.3 (minimumInteractiveComponentSize is long stable).
// Opt-ins: none.
// Resources assumed: R.string.favorite, state_favorite, state_not_favorite, rating_label;
//   R.plurals.rating_stars ("%d star" / "%d stars"); R.drawable.ic_star, ic_star_filled.
// Prefer the standard components (IconToggleButton, Slider, RadioButton) when their look is
// acceptable: they already do all of this.
//
// Pages applied:
//   https://developer.android.com/develop/ui/compose/accessibility/api-defaults
//   https://developer.android.com/develop/ui/compose/accessibility/semantics
//   https://developer.android.com/develop/ui/compose/accessibility/merging-clearing
//   https://m3.material.io/foundations/accessible-design/overview
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.foundation.selection.toggleable
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.minimumInteractiveComponentSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.pluralStringResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription

@Composable
fun FavoriteToggle(favorite: Boolean, onFavoriteChange: (Boolean) -> Unit, modifier: Modifier = Modifier) {
    val label = stringResource(R.string.favorite)
    val state = stringResource(if (favorite) R.string.state_favorite else R.string.state_not_favorite)
    Box(
        modifier = modifier
            // toggleable gives click handling, focus, the Switch role, the on/off state and
            // merges the child icon into this one node.
            .toggleable(value = favorite, role = Role.Switch, onValueChange = onFavoriteChange)
            // Reserves at least 48dp x 48dp although the icon is 24dp. It comes after
            // toggleable so that the whole reserved area responds to touch.
            .minimumInteractiveComponentSize()
            .semantics {
                // The name says what the control is, never its role or state ("button", "on").
                contentDescription = label
                // Replaces the generic "on/off" with wording that fits the control.
                stateDescription = state
            },
        contentAlignment = Alignment.Center,
    ) {
        Icon(
            // State is carried by shape (filled versus outlined star), not only by tint.
            painter = painterResource(if (favorite) R.drawable.ic_star_filled else R.drawable.ic_star),
            contentDescription = null, // decorative here: the parent node carries the label
            // Colors come from theme roles so they hold up in dark theme and dynamic color.
            tint = if (favorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
fun StarRating(rating: Int, onRatingChange: (Int) -> Unit, modifier: Modifier = Modifier, max: Int = 5) {
    val groupLabel = stringResource(R.string.rating_label)
    Row(
        // selectableGroup marks the stars as one set of mutually exclusive options; the
        // description names the set when focus first enters it.
        modifier = modifier.selectableGroup().semantics { contentDescription = groupLabel },
    ) {
        for (value in 1..max) {
            val starLabel = pluralStringResource(R.plurals.rating_stars, value, value)
            Box(
                modifier = Modifier
                    // One option per star, exposed like a radio button: "3 stars, selected,
                    // radio button". Works with touch, keyboard, switch and TalkBack
                    // without any custom gesture.
                    .selectable(
                        selected = value == rating,
                        role = Role.RadioButton,
                        onClick = { onRatingChange(value) },
                    )
                    .minimumInteractiveComponentSize() // 48dp per star, so targets never overlap
                    .semantics { contentDescription = starLabel },
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    // Stars up to the rating are filled, the rest outlined: readable without
                    // color perception and in high-contrast modes.
                    painter = painterResource(if (value <= rating) R.drawable.ic_star_filled else R.drawable.ic_star),
                    contentDescription = null,
                    tint = if (value <= rating) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
