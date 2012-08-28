package com.google.lint.check;

import com.google.common.base.Joiner;
import com.google.common.collect.ImmutableSet;
import com.google.inject.Inject;
import com.google.lint.common.Context;
import com.google.lint.common.FamilyMetadata;
import com.google.lint.common.FontMetadata;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;
import com.google.lint.common.Severity;

import java.io.File;
import java.util.List;
import java.util.Set;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckCanonicalStyleNames implements LintCheck {

  private static final Set<String> CANONICAL_STYLE_VALUES = ImmutableSet.<String>builder()
      .add("normal")
      .add("italic")
      .build();
  private static final String CANONICAL_STYLE_VALUES_STRING = Joiner.on(", ")
      .join(CANONICAL_STYLE_VALUES);

  private final MetadataStore metadataStore;

  @Inject
  public CheckCanonicalStyleNames(MetadataStore metadataStore) {
    this.metadataStore = metadataStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        String fontStyle = fontMetadata.getStyle();
        if (!CANONICAL_STYLE_VALUES.contains(fontStyle)) {
          context.report(Severity.ERROR,
              String.format("%s: Style is \"%s\" for %s which is not one of the canonical values" +
              " (%s)", new File(familyDirectory, "METADATA.json").getPath(), fontStyle,
              fontMetadata.getFilename(), CANONICAL_STYLE_VALUES_STRING));
        }
      }
    }
  }
}
